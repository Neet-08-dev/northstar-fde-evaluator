# Northstar — PRIVATE evaluator repository

Keep this repository restricted to the hiring team. Never put it in the candidate repository, a candidate branch, a candidate-visible CI job or the submitted container. Baseline: 72 hidden cases, eight categories, three independent trials by default. Six phase-2 packs add 18 targeted acceptance cases.

## GitHub access and candidate handoff

The candidate starter is a separate public template repository, `northstar-fde-candidate`. This evaluator is a private repository, `northstar-fde-evaluator`. Invite only interviewers to this repository. Its tests and calibration workflow run privately; keep candidate grading runs and reports private too.

For each candidate, create a **Private** repository from the public starter's **Use this template** button, such as `fde-submission-017`. Invite only that candidate and the hiring team to the submission repository. Share the brief, deadline, agreed model budget and published scoring dimensions. Candidates may instead create their own private template copy and grant you access. A fork of a public repository remains public, so use template copies for private submissions.

At submission, record the repository URL and exact commit SHA. Clone and check out that commit, then use it as the build source below. Keep the private evaluator, hidden cases and reports outside the submitted repository. Run one phase-2 change using `phase2/README.md`, complete the human scorecard, and share feedback without disclosing the hidden suite or answer traces.

## Calibrate without Docker or model keys
Python 3.12+; no packages to install:

```sh
python -m unittest discover -s tests -v
python run_assessment.py --self-check --trials 3 --report-dir reports/calibration
```

Self-check executes evaluator-only authored reference traces against the actual HTTP mock API. It proves fixtures and grader behavior, not that a production AI solution works. The submitted agent is never given those reference traces. Tests also reject fabricated actions, unauthorized attempts, malformed responses and extra financial effects.

## Run a candidate with Docker
Keep the two repositories beside each other; use the candidate's exact submitted commit as the build source. Review their Dockerfile and dependency/start requirements first.

```sh
python setup_local.py
docker build -t northstar-submission:local ../northstar-candidate
docker compose up --build -d mock-api candidate-agent
docker compose run --rm grader python run_assessment.py --agent-url http://candidate-agent:8000 --api-url http://mock-api:8001 --candidate-id FDE-017 --trials 3 --report-dir /reports/FDE-017
docker compose down
```

For a cloned submission in another directory, replace the build path. Put only necessary model/provider secrets in `.candidate.env`. The separate generated `.env` admin secret goes only to the trusted mock and grader. The candidate container has no hidden-data/reports mounts, host port, Docker socket or admin token; it receives one scoped capability per `/process` call. It may have outbound network access for model providers. Candidate health checks can be adapted to their runtime without changing grading logic. Default resources are two CPUs, 1 GB RAM and a writable `/tmp`; agree changes consistently across candidates.

Images run as independent containers and the trusted mock is built only from `trusted_world`. The private Python runner is a separate process. Docker is a convenient boundary for cooperative submissions, not a hardened hostile-code sandbox; use a disposable machine for untrusted code. Provider tokens should have a hiring-only budget. This operational constraint matters because a submitted Dockerfile executes code during build.

## Run an already-hosted agent

Start the trusted API from this repository, not the submitted mock. Set ADMIN_TOKEN to a fresh local value in the environment and use PYTHONPATH=trusted_world:

```sh
PYTHONPATH=trusted_world python -m northstar.api --host 127.0.0.1
python run_assessment.py --agent-url http://localhost:8000 --api-url http://localhost:8001 --candidate-id FDE-017 --trials 3 --report-dir reports/FDE-017
```

PowerShell: `$env:PYTHONPATH='trusted_world'` before starting the API; `$env:ADMIN_TOKEN` must be set in both API and runner terminals. If the agent is in a container, use `--agent-api-url http://host.docker.internal:8001` and bind the mock to an address reachable from that container; restrict that local port appropriately. Docker Compose avoids this address mismatch.

## Reports and human scoring
Read `reports/FDE-017/report.md`, `report.json` and private `trials.json`. The latter contains server audit, final state, responses and failure reasons. Never share it with a candidate while the suite is in use. Check critical flags first. Automatic points total 60; 40 remain pending until evidence-backed review.

Copy `scoring/review_template.json`, enter rubric points/evidence, and optionally adjudicate communication false positives with case ID, trial, a 0..1 score and reason. Rerun the same model/configuration/seed with `--manual-review your-review.json`; keep the original report alongside it because new model trials may differ. To add review to an existing run without new trials, use `python score_existing.py --report-dir reports/FDE-017 --review your-review.json`.

```sh
python run_assessment.py --self-check --suite phase2/cases/01_credit_approval.json --trials 3 --report-dir reports/phase2-calibration
```

Replace --self-check with the candidate/API arguments to grade the live change. `--case-id` and `--category` can be repeated for focused investigation. Do not tune hidden cases to one candidate after seeing their scores. Pin the candidate commit, suite hash, model settings, budget and harness version for comparisons.

Read `scoring/SCORECARD.md`, `interview/INTERVIEWER_GUIDE.md`, `reference/EXPECTATIONS.md` and `phase2/README.md` before using results for hiring. There is no automatic hire/no-hire decision. Missing cost telemetry is unknown, not free. Communication checks are heuristics, and automated checks cannot prove absence of all prompt injection or exfiltration.
