import json
from pathlib import Path

RUBRIC_WEIGHTS = {'problem_design': 10, 'evaluation_methodology': 15, 'ai_build_workflow': 10, 'code_demo': 5}


def apply_review(report, path, rows):
    review = json.loads(Path(path).read_text(encoding='utf-8'))
    if review.get('candidate_id') and review['candidate_id'] != report.get('candidate_id'):
        raise ValueError('Review candidate_id does not match the report')
    rubric = review.get('rubric', {})
    points = 0
    pending = []
    for key, weight in RUBRIC_WEIGHTS.items():
        entry = rubric.get(key, {})
        score = entry.get('score')
        if score is None:
            pending.append(key)
            continue
        if type(score) not in [int, float] or not 0 <= score <= weight or not entry.get('evidence', '').strip():
            raise ValueError('Manual score requires range-valid points and evidence: ' + key)
        points += score
    report['manual_review'] = review
    report['manual_pending'] = pending
    if review.get('human_safety_observations'):
        report['decision'] = 'Review required: human safety observations'
    if not pending:
        report['manual_points'] = points
        report['overall_points'] = round(report['automatic_points'] + points, 4)
    return report
