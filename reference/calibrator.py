"""Execute authored traces to prove cases are achievable. This is an oracle, not an AI solution."""
import copy

from northstar.http import ToolClient, RemoteError
from northstar.world import utc
from graders.common import WRITES


def execute(case, payload):
    client = ToolClient(payload['api_url'], payload['session_token'])
    context, policy = client.call('get_context'), client.call('get_policy')
    evidence = [{'collection': 'policy', 'record_id': policy['rules']['version']}]
    saved = {}
    for record in case['expect'].get('reads', []):
        client.call('get_record', collection=record['collection'], record_id=record['record_id'])
        evidence.append(record)

    def resolve(value):
        if isinstance(value, str) and value.startswith('$'):
            name, key = value[1:].split('.', 1)
            return saved[name][key]
        return value

    def call_retry(name, args, allow_failure=False, refresh_version=False):
        for attempt in range(3):
            try:
                return client.call(name, **args)
            except RemoteError as exc:
                if refresh_version and exc.error['code'] == 'VERSION_CONFLICT':
                    current = client.call('get_record', collection='tickets', record_id=args['ticket_id'])
                    args['expected_version'] = current['version']
                    # Version refresh changes logical arguments; the first attempt never committed.
                    args['idempotency_key'] += '-refreshed'
                    continue
                if not exc.error.get('retryable') or attempt == 2:
                    if allow_failure:
                        return None
                    raise
        raise RuntimeError('Unreachable retry state')

    collection_map = {'create_ticket': 'tickets', 'update_ticket': 'tickets', 'schedule_visit': 'visits',
                      'issue_credit': 'credits', 'request_approval': 'approvals', 'draft_message': 'drafts', 'escalate': 'escalations'}
    for index, instruction in enumerate(case['reference']['steps']):
        if 'choose_slot' in instruction:
            target = instruction['choose_slot']
            slots = client.call('list_slots', asset_id=target['asset_id'])['slots']
            selected = next((s for s in slots if (not target.get('starts_at') or utc(s['starts_at']) == utc(target['starts_at'])) and
                             (not target.get('technician_id') or s['technician_id'] == target['technician_id'])), None)
            if selected is None:
                raise RuntimeError('Reference fixture has no matching slot')
            name = 'schedule_visit'
            args = {'ticket_id': resolve(target['ticket_id']), 'technician_id': selected['technician_id'], 'starts_at': selected['starts_at']}
        else:
            name = instruction['tool']
            args = {k: resolve(v) for k, v in instruction['arguments'].items()}
        if name in WRITES:
            args['idempotency_key'] = payload['run_id'] + '-action-' + str(index)
        value = call_retry(name, args, instruction.get('allow_failure', False), instruction.get('refresh_version', False))
        if value and name in collection_map:
            evidence.append({'collection': collection_map[name], 'record_id': value['id']})
        if instruction.get('save_as'):
            saved[instruction['save_as']] = copy.deepcopy(value)
    return {'status': case['reference']['status'], 'summary': case['reference']['reply'], 'reply': case['reference']['reply'],
            'evidence': evidence, 'usage': {'model': 'none', 'input_tokens': 0, 'output_tokens': 0, 'cost_usd': 0, 'pricing_source': 'Calibration oracle, no model calls'}}
