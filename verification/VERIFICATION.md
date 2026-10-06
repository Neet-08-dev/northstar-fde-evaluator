# Verification — October 6, 2026

The two packages were authored from scratch in this workspace using fictional commercial field-services entities. No private project files, schemas or business logic were accessed or reused. No remote GitHub repositories have been created.

| Check | Actual result |
|---|---|
| Candidate contract/HTTP/security tests | 16 passed on Python 3.12.14 |
| Private grader/fairness/integrity/manual-score tests | 20 passed on Python 3.12.14 |
| Base hidden calibration | 72 cases × 3 trials = 216 passes; automatic calibration score 60/60 |
| Live-change calibration | 6 packs × 3 cases × 3 trials = 54 passes |
| Public reference outcomes | All eight verified against the real HTTP tool API |
| Unimplemented starter control | Actual HTTP starter fails all eight public tasks and all 216 hidden trials, as expected |
| Fabricated action control | Claim-only responses fail all 72 hidden cases |
| Human scoring | Missing points stay pending; complete synthetic ratings sum correctly to 100 and preserve safety-review flags |
| Existing-run review command | Runs without resampling and leaves original reports intact |
| Docker Compose configuration | Both configurations validate with installed Compose 5.4.0 |
| Docker image build/container execution | **Unverified: installed Docker client cannot reach a running engine on this machine** |

Calibration uses evaluator-only authored traces to prove fixtures are feasible and graders recognize expected behavior. It is not a candidate AI solution, a model benchmark or evidence of production readiness. An independent code review found four issues in scheduling fairness and malformed-input handling; regression tests now accept equivalent UTC offsets and equally qualified technicians, reject later slots when earliest is required, and handle malformed replies/oversized telemetry as failures.

During validation, an intermittent HTTP connection reset was traced to administrative/authentication responses that closed before consuming their request bodies. The API now consumes and validates POST bodies before responding; regression tests cover finalization payloads, malformed JSON and denied administrative requests. No interrupted run was represented as a candidate score. For hiring use, run each candidate in a disposable environment with a pinned commit, equal budget and the original trusted mock.

Automatic scoring totals 60 points. The remaining 40 require evidence-backed human ratings. Cost is self-reported; automatic efficiency uses measured latency and API attempts. Communication grading is an explicit heuristic with recorded human adjudication. Safety flags require review regardless of aggregate score.

The evaluator contains sample calibration/control reports under verification/. Full generated run traces remain in the local ignored reports/ directory and are excluded from the source archive. Candidate archives exclude private cases, graders, traces, secrets and Git metadata. Source archives and checksum manifest are supplied beside this document.
