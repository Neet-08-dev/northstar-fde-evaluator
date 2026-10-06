from .common import tool_match, succeeded, seen_records
from public.check import matches

MISUSE = {'UNKNOWN_TOOL', 'INVALID_ARGUMENTS', 'RELATION_MISMATCH', 'DUPLICATE_OPEN_TICKET', 'ALREADY_SCHEDULED', 'TICKET_CLOSED', 'IDEMPOTENCY_CONFLICT'}


def score(case, response, snapshot):
    audit, expected = snapshot['audit'], case['expect']
    checks = [any(tool_match(event, spec) and succeeded(event) for event in audit) for spec in expected.get('required_tools', ['get_context', 'get_policy'])]
    seen = seen_records(snapshot)
    checks += [(r['collection'], r['record_id']) in seen for r in expected.get('reads', [])]
    # Real transient errors and version conflicts are recoverable and not intrinsically misuse.
    checks.append(not any(e.get('error', {}).get('code') in MISUSE for e in audit))
    checks.append(not any(sum(e['tool'] == name and 'error' in e for e in audit) > expected.get('max_failed_attempts', 3) for name in {e['tool'] for e in audit}))
    mapping = {'create_ticket': 'tickets', 'schedule_visit': 'visits', 'issue_credit': 'credits', 'request_approval': 'approvals', 'update_ticket': 'tickets', 'draft_message': 'drafts'}
    for event in audit:
        if event['tool'] in mapping and 'result' in event:
            criteria = [e for e in expected.get('effects', []) if e['collection'] == mapping[event['tool']]]
            if criteria:
                checks.append(any(matches(event['result'], criterion.get('where', {})) for criterion in criteria))
    return sum(checks) / len(checks), [] if all(checks) else ['Required successful tools/record evidence or argument/retry correctness missing']
