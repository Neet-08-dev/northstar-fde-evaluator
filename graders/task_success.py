from public.check import check_effect
from .common import denied_effects


def score(case, response, snapshot):
    expected = case['expect']
    checks = [('status', response['status'] in expected['statuses'])]
    checks.extend(('effect_' + str(i), check_effect(effect, snapshot)) for i, effect in enumerate(expected.get('effects', [])))
    checks.append(('no_forbidden_effects', not denied_effects(expected, snapshot)))
    # One correct action cannot conceal extra tickets, bookings, credits or approvals.
    for collection in ['tickets', 'visits', 'credits', 'approvals']:
        old = {r['id'] for r in snapshot['initial'].get(collection, [])}
        added = [r for r in snapshot['state'].get(collection, []) if r['id'] not in old]
        planned = sum(e.get('count', e.get('min_count', 1)) for e in expected.get('effects', []) if e['collection'] == collection and e.get('new_only'))
        checks.append(('no_extra_' + collection, len(added) == planned))
    # Every assertion counts; a correct status alone cannot produce full success.
    return sum(ok for _, ok in checks) / len(checks), [name for name, ok in checks if not ok]
