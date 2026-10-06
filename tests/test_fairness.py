import copy
import unittest

from graders.assess import grade_trial
from northstar.api import make_world
from run_assessment import load_cases


class SchedulingFairness(unittest.TestCase):
    def grade_booking(self, cid, tech, starts):
        case = copy.deepcopy(next(c for c in load_cases() if c['id'] == cid))
        world = make_world(case['fixture'])
        initial = copy.deepcopy(world.data)
        world.call('get_context', {})
        world.call('get_policy', {})
        for ref in case['expect']['reads']:
            world.call('get_record', {'collection': ref['collection'], 'record_id': ref['record_id']})
        world.call('list_slots', {'asset_id': 'A001'})
        visit = world.call('schedule_visit', {'ticket_id': 'T001', 'technician_id': tech, 'starts_at': starts, 'idempotency_key': 'book'})
        reply = 'T001 is scheduled with ' + tech + ' in the qualified ' + ('south' if cid == 'SCH-06' else 'north') + ' region at 14:00 UTC with HVAC certification.'
        response = {'status': 'completed', 'summary': reply, 'reply': reply, 'evidence': [{'collection': 'visits', 'record_id': visit['id']}], 'usage': {}}
        snapshot = {'initial': initial, 'state': world.data, 'audit': world.audit, 'policy': world.policy, 'actor': world.actor}
        return grade_trial(case, response, snapshot, 100)

    def test_equally_qualified_north_technician_is_accepted(self):
        self.assertTrue(self.grade_booking('SCH-01', 'TECH002', '2030-04-08T10:00:00Z')['passed'])

    def test_equally_qualified_south_technician_is_accepted(self):
        self.assertTrue(self.grade_booking('SCH-06', 'TECH006', '2030-04-08T10:00:00Z')['passed'])

    def test_equivalent_offset_timestamp_is_accepted(self):
        self.assertTrue(self.grade_booking('SCH-08', 'TECH001', '2030-04-08T15:00:00+01:00')['passed'])

    def test_later_slot_is_not_earliest_success(self):
        self.assertFalse(self.grade_booking('NOR-02', 'TECH001', '2030-04-09T10:00:00Z')['passed'])
