# Phase 2: choose one 45-minute live change

There are six candidate-facing cards in `requests/` and six PRIVATE three-case acceptance suites in `cases/`. Baseline hidden cases remain unchanged. Give the candidate the chosen card and the described runtime policy/fixture updates; do not give the private case JSON, reference traces or expected replies. The updates use the public admin fixture format in docs/API.md and the existing tool interface.

Run `python run_assessment.py --suite phase2/cases/01_credit_approval.json` with the normal candidate/API arguments and --trials 3 after the change. Self-check supports each suite without model keys. Re-run a small baseline regression subset plus the candidate's added evals. Keep phase-2 scores separate from the take-home score; evaluate the live work using interview evidence, not a silently changed 100-point weighting.

Suggested live review: 0-5 understand the update and acceptance bar; 5-35 implement and verify; 35-45 demonstrate the revised behavior, a regression and known limits. Coding assistants are allowed. Reward the candidate who changes the correct boundary, adds an independent eval and acknowledges unresolved behavior.
