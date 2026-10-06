import json
import tempfile
import unittest
from pathlib import Path

from scoring.manual import apply_review


class EvidenceBasedManualScoring(unittest.TestCase):
    def test_completed_review_produces_100_and_preserves_safety_flag(self):
        review = {'candidate_id': 'synthetic-control', 'rubric': {k: {'score': points, 'evidence': 'Synthetic test evidence'} for k, points in
                 [('problem_design', 10), ('evaluation_methodology', 15), ('ai_build_workflow', 10), ('code_demo', 5)]}, 'human_safety_observations': ['Synthetic critical observation']}
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'review.json'
            path.write_text(json.dumps(review), encoding='utf-8')
            report = {'automatic_points': 60, 'candidate_id': 'synthetic-control', 'decision': 'Human review pending'}
            apply_review(report, path, [])
            self.assertEqual(report['overall_points'], 100)
            self.assertIn('Review required', report['decision'])

    def test_review_requires_evidence_and_correct_candidate(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'review.json'
            path.write_text(json.dumps({'candidate_id': 'wrong', 'rubric': {}}), encoding='utf-8')
            with self.assertRaises(ValueError):
                apply_review({'automatic_points': 30, 'candidate_id': 'right'}, path, [])
