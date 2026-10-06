import copy
import json
import unittest
from pathlib import Path

from graders.assess import grade_trial, WEIGHTS
from northstar.api import make_world
from northstar.schema import TOOLS
from run_assessment import load_cases, verify_baseline
from scoring.manual import RUBRIC_WEIGHTS, apply_review

ROOT = Path(__file__).resolve().parents[1]


class SuiteIntegrityTests(unittest.TestCase):
    def test_baseline_is_hash_pinned(self):
        verify_baseline()

    def test_72_distinct_cases_and_valid_fixture_references(self):
        cases = load_cases()
        self.assertEqual(len(cases), 72)
        self.assertEqual(len({c['request']['body'] for c in cases}), 72)
        self.assertEqual(len({c['category'] for c in cases}), 8)
        for case in cases:
            world = make_world(case['fixture'])
            ids = {(name, row['id']) for name, rows in world.data.items() for row in rows}
            for record in case['expect'].get('reads', []):
                self.assertIn((record['collection'], record['record_id']), ids, case['id'])
            for name in case['expect']['required_tools']:
                self.assertIn(name, TOOLS)

    def test_weighted_score_is_exactly_100(self):
        self.assertEqual(sum(WEIGHTS.values()) + sum(RUBRIC_WEIGHTS.values()), 100)

    def test_missing_manual_review_does_not_create_a_total(self):
        report = {'automatic_points': 60, 'candidate_id': 'sample'}
        apply_review(report, ROOT / 'scoring/review_template.json', [])
        self.assertNotIn('overall_points', report)
        self.assertEqual(len(report['manual_pending']), 4)

    def test_claim_only_mutant_fails_every_hidden_case(self):
        for case in load_cases():
            world = make_world(case['fixture'])
            snapshot = {'initial': copy.deepcopy(world.data), 'state': copy.deepcopy(world.data), 'audit': [], 'policy': world.policy, 'actor': world.actor}
            output = {'status': case['reference']['status'], 'summary': 'Everything completed', 'reply': case['reference']['reply'], 'evidence': [], 'usage': {'cost_usd': 0}}
            self.assertFalse(grade_trial(case, output, snapshot, 1)['passed'], case['id'])

    def test_phase2_has_six_three_case_packs(self):
        packs = list((ROOT / 'phase2/cases').glob('*.json'))
        self.assertEqual(len(packs), 6)
        for path in packs:
            self.assertEqual(len(json.loads(path.read_text(encoding='utf-8'))), 3)
