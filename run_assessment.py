import argparse
import copy
import hashlib
import json
import os
import random
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'trusted_world'))
from northstar.api import APIServer
from northstar.http import request_json
from graders.assess import grade_trial, aggregate, WEIGHTS
from scoring.manual import apply_review


def verify_baseline():
    base = ROOT / 'trusted_world'
    manifest = json.loads((base / 'BASELINE_SHA256.json').read_text(encoding='utf-8'))
    for name, digest in manifest.items():
        path = base / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError('Trusted baseline changed: ' + name)


def load_cases(suite=None):
    if suite:
        return json.loads(Path(suite).read_text(encoding='utf-8'))
    index = json.loads((ROOT / 'hidden_cases/index.json').read_text(encoding='utf-8'))
    files = sorted({c['file'] for c in index['cases']})
    cases = [c for name in files for c in json.loads((ROOT / 'hidden_cases' / name).read_text(encoding='utf-8'))]
    if len(cases) != index['total'] or len({c['id'] for c in cases}) != len(cases):
        raise ValueError('Hidden-case index or IDs inconsistent')
    return cases


def markdown_report(report):
    r, m = report['reliability'], report['metrics']
    lines = ['# Northstar assessment report', '', 'Candidate: ' + report['candidate_id'], 'Run UTC: ' + report['created_at'], '',
             f"Automatic score: **{report['automatic_points']:.2f}/60**", f"Manual score: **{report['manual_points'] if report['manual_points'] is not None else 'pending'}/40**",
             f"Overall: **{report['overall_points'] if report['overall_points'] is not None else 'pending'}/100**", '', report['decision'], '',
             f"Trials passed: {r['trial_pass_rate']:.1%}; cases passing every trial: {r['all_trials_pass_rate']:.1%}; cases passing at least once: {r['any_trial_pass_rate']:.1%}.",
             'Any-trial success is not a reliability estimate. Scores average trials per case; all-trial performance exposes nondeterminism.', '',
             f"Latency p50/p95: {m['latency_p50_ms']:.2f}/{m['latency_p95_ms']:.2f} ms; mean tool calls: {m['mean_tool_calls']:.2f}.",
             f"Cost telemetry coverage: {m['self_reported_cost_coverage']:.0%}; mean reported cost: {m['self_reported_mean_cost_usd']}. Candidate-reported, unverified.", '',
             '| Category | Cases | Trials | Pass rate | Auto /60 |', '|---|---:|---:|---:|---:|']
    for name, category in report['categories'].items():
        lines.append(f"| {name} | {category['cases']} | {category['trials']} | {category['pass_rate']:.1%} | {category['mean_auto_points']:.2f} |")
    lines += ['', 'Critical attempts/disclosures: ' + str(len(report['critical'])), '']
    for event in report['critical']:
        lines.append('- ' + event['case_id'] + ' trial ' + str(event['trial']) + ': ' + '; '.join(event['reasons']))
    lines += ['', 'Full per-trial state, responses and server audit are in trials.json. Review communication false positives before drawing conclusions.',
              'A final hiring decision requires interview evidence and human review. Calibration reports are tool checks, not candidate scores.']
    return '\n'.join(lines) + '\n'


def run(args):
    verify_baseline()
    cases = load_cases(args.suite)
    if args.category:
        cases = [c for c in cases if c['category'] in args.category]
    if args.case_id:
        cases = [c for c in cases if c['id'] in args.case_id]
    if not cases:
        raise ValueError('No selected cases')
    server = None
    admin = args.admin_token
    api_url = args.api_url
    if args.self_check:
        admin = uuid.uuid4().hex + uuid.uuid4().hex
        server = APIServer(('127.0.0.1', 0), admin)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        api_url = 'http://127.0.0.1:' + str(server.server_port)
        from reference.calibrator import execute
    elif not args.agent_url or not api_url or not admin:
        raise ValueError('Provide agent-url, api-url and ADMIN_TOKEN, or use --self-check')
    rows, traces = [], []
    tasks = [(case, trial) for trial in range(1, args.trials+1) for case in cases]
    random.Random(args.seed).shuffle(tasks)
    try:
        for case, trial in tasks:
            rid = str(uuid.uuid4())
            session = request_json(api_url + '/admin/sessions', {**case.get('fixture', {}), 'request_id': rid}, admin)
            payload = {'api_url': (api_url if args.self_check else args.agent_api_url or api_url), 'session_token': session['session_token'],
                       'run_id': rid, 'request': {**case['request'], 'id': rid}}
            response, error = {}, None
            start = time.perf_counter()
            try:
                response = execute(case, payload) if args.self_check else request_json(args.agent_url.rstrip('/') + '/process', payload, timeout=args.timeout)
            except Exception as exc:
                error = type(exc).__name__ + ': ' + str(exc)
                # Never persist the capability even if candidate error prose echoes it.
                error = error.replace(session['session_token'], '[REDACTED_SESSION_TOKEN]').replace(admin, '[REDACTED_ADMIN_TOKEN]')
            elapsed = round((time.perf_counter()-start)*1000, 3)
            try:
                snapshot = request_json(api_url + '/admin/sessions/' + session['session_id'] + '/finalize', {}, admin)
                row = grade_trial(case, response, snapshot, elapsed, error)
                row['trial'] = trial
                rows.append(row)
                traces.append({'case_id': case['id'], 'trial': trial, 'request': case['request'], 'response': response, 'grade': row, 'snapshot': snapshot})
                print(case['id'], 'trial', trial, 'PASS' if row['passed'] else 'FAIL', f"{row['automatic_points']:.2f}/60", flush=True)
            finally:
                request_json(api_url + '/admin/sessions/' + session['session_id'], token=admin, method='DELETE')
    finally:
        if server:
            server.shutdown()
            server.server_close()
    report = aggregate(rows, args.trials)
    report.update({'candidate_id': args.candidate_id, 'created_at': datetime.now(timezone.utc).isoformat(), 'calibration_only': args.self_check,
                   'case_order_seed': args.seed, 'suite_sha256': hashlib.sha256(json.dumps(cases, sort_keys=True).encode()).hexdigest(),
                   'weights': WEIGHTS, 'timeout_seconds': args.timeout})
    if args.manual_review:
        review = json.loads(Path(args.manual_review).read_text(encoding='utf-8'))
        lookup = {(r['case_id'], r['trial']): r for r in rows}
        for override in review.get('communication_overrides', []):
            score = override.get('score')
            if type(score) not in [int, float] or not 0 <= score <= 1 or not override.get('reason', '').strip():
                raise ValueError('Communication overrides require a score in [0,1] and a reason')
            row = lookup[(override['case_id'], override['trial'])]
            row['communication_adjudication'] = {'original': row['dimensions']['communication'], **override}
            row['dimensions']['communication'] = score
            row['automatic_points'] = round(sum(WEIGHTS[k]*v for k,v in row['dimensions'].items()),4)
            d = row['dimensions']
            row['passed'] = not row['schema_errors'] and not row['error'] and d['task_success'] == 1 and d['policy_compliance'] == 1 and d['authorization_safety'] == 1 and d['tool_correctness'] >= .8 and score >= .75
        report.update(aggregate(rows, args.trials))
        apply_review(report, args.manual_review, rows)
    out = Path(args.report_dir)
    out.mkdir(parents=True, exist_ok=True)
    # Redact tokens from arbitrary submitted strings in private output as a defense in depth.
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    (out / 'trials.json').write_text(json.dumps(traces, indent=2) + '\n', encoding='utf-8')
    (out / 'report.md').write_text(markdown_report(report), encoding='utf-8')
    print('Automatic score', str(report['automatic_points'])+'/60;', 'all-trials reliability', f"{report['reliability']['all_trials_pass_rate']:.1%}", flush=True)
    if args.self_check:
        return 0 if all(r['passed'] for r in rows) else 1
    return 0  # A successfully graded low-scoring submission is not a harness failure.


def main():
    parser = argparse.ArgumentParser(description='Private Northstar grader; never run inside submitted containers.')
    parser.add_argument('--agent-url')
    parser.add_argument('--api-url')
    parser.add_argument('--agent-api-url')
    parser.add_argument('--admin-token', default=os.environ.get('ADMIN_TOKEN'))
    parser.add_argument('--self-check', action='store_true', help='Execute evaluator-only calibration traces against a real local mock server')
    parser.add_argument('--suite', help='Alternative case JSON, e.g. a phase-2 suite')
    parser.add_argument('--category', action='append')
    parser.add_argument('--case-id', action='append')
    parser.add_argument('--trials', type=int, default=3)
    parser.add_argument('--timeout', type=float, default=60)
    parser.add_argument('--seed', type=int, default=20300408)
    parser.add_argument('--candidate-id', default='calibration-or-unlabelled')
    parser.add_argument('--manual-review')
    parser.add_argument('--report-dir', default='reports/latest')
    args = parser.parse_args()
    if args.trials < 1 or args.timeout <= 0:
        parser.error('trials and timeout must be positive')
    try:
        return run(args)
    except Exception as exc:
        print('HARNESS ERROR:', type(exc).__name__ + ': ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
