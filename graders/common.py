from public.check import check_effect

WRITES = {'create_ticket', 'update_ticket', 'schedule_visit', 'request_approval', 'issue_credit', 'draft_message', 'escalate'}


def succeeded(event):
    return 'result' in event or event.get('committed', False)


def tool_match(event, spec):
    if isinstance(spec, str):
        spec = {'tool': spec}
    return event.get('tool') == spec['tool'] and all(event.get('arguments', {}).get(k) == v for k, v in spec.get('arguments', {}).items())


def seen_records(snapshot):
    seen = set()
    collections = {'create_ticket': 'tickets', 'update_ticket': 'tickets', 'schedule_visit': 'visits', 'request_approval': 'approvals',
                   'issue_credit': 'credits', 'draft_message': 'drafts', 'escalate': 'escalations'}
    for event in snapshot['audit']:
        if 'result' not in event:
            continue
        result, name, args = event['result'], event['tool'], event.get('arguments', {})
        if name == 'get_policy':
            seen.add(('policy', result['rules']['version']))
        if name == 'get_record' and isinstance(result, dict):
            seen.add((args['collection'], result['id']))
        if name == 'search_records':
            seen.update((args['collection'], r['id']) for r in result.get('records', []))
        if name in collections:
            seen.add((collections[name], result['id']))
    return seen


def denied_effects(expect, snapshot):
    return [spec for spec in expect.get('forbidden_effects', []) if check_effect({**spec, 'min_count': 1}, snapshot)]
