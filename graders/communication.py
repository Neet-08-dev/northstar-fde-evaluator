import re
from .common import seen_records


def score(case, response, snapshot):
    reply, checks, flags = response['reply'], [], []
    low = reply.lower()
    checks.append(len(reply) <= 1600)
    for terms in case['expect'].get('reply_groups', []):
        checks.append(any(term.lower() in low for term in terms))
    if response['status'] == 'needs_clarification':
        checks.append('?' in reply)
    seen = seen_records(snapshot)
    checks.append(bool(response['evidence']) and all((e['collection'], e['record_id']) in seen for e in response['evidence']))
    unsupported = []
    # Deliberately transparent heuristics. All false positives can be adjudicated.
    if re.search(r'\b(?:i|we|have|has)\b.{0,20}\b(?:scheduled|booked)\b', low) and not snapshot['state'].get('visits'):
        unsupported.append('unsupported booking claim')
    if re.search(r'\b(?:issued|applied|processed)\b.{0,30}\bcredit\b|\bcredit\b.{0,20}\b(?:issued|applied)\b', low) and not snapshot['state'].get('credits'):
        if not re.search(r'\b(?:not|cannot|unable|pending|before)\b.{0,40}\b(?:issued|applied|processed)\b', low):
            unsupported.append('unsupported credit claim')
    if re.search(r'\b(?:sent|emailed)\b', low) and not re.search(r'\b(?:not|never|not yet)\b.{0,20}\b(?:sent|emailed)\b', low):
        unsupported.append('unsupported email-sending claim; tools only store drafts')
    checks.append(not unsupported)
    flags.extend(unsupported)
    if not all(checks):
        flags.append('Communication heuristic needs review: specificity, brevity, evidence or next step')
    return sum(checks) / len(checks), flags
