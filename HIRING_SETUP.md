# Northstar forward-deployed AI engineer assessment

Everything is fictional commercial field services data authored from scratch. These packages have no dependency on any private project.

| Package | Who receives it | Contents |
|---|---|---|
| northstar-candidate | Candidates | Brief, data, policies, mock tools, starter, Docker, eight public scenarios, submission templates |
| northstar-evaluator | Hiring team only | 72 hidden cases, grader, repeated trials, 100-point scorecard, interview guide, six live changes with 18 private checks |

## Distribute through GitHub
The [candidate repository](https://github.com/Neet-08-dev/northstar-fde-candidate) is a public template. The [evaluator repository](https://github.com/Neet-08-dev/northstar-fde-evaluator) is private and belongs to the same hiring account, `Neet-08-dev`. Keep the evaluator restricted to interviewers; never store it in another branch of the candidate repository. Each package includes a .gitignore that excludes secrets and run reports.

Interviewers can clone the packages into matching local directories:

```sh
git clone https://github.com/Neet-08-dev/northstar-fde-candidate.git northstar-candidate
git clone https://github.com/Neet-08-dev/northstar-fde-evaluator.git northstar-evaluator
```

The evaluator clone requires a GitHub login with access to the private repository. Grant that access only to the hiring team through its **Settings → Collaborators**.

For each candidate, open the public template and select **Use this template → Create a new repository**. Create a private repository such as `fde-submission-017` under the hiring account, then invite that candidate as a collaborator from that submission repository's Settings. Give them its link, timebox and due date. A private submission can also live in the candidate's account if they grant the hiring team access. Use the template feature: GitHub forks of a public repository stay public.

Only interviewers get access to the private evaluator. Keep grading reports, hidden cases, review notes and model keys there or in ignored local files. Each candidate gets access only to their own submission repository. Review the latest submitted commit, then privately build and grade that exact commit using the evaluator below.

Agree a recommended compensated six-hour timebox and a shared model budget. Give candidates their repo, its README/brief, the published scoring dimensions and a due date. Explicitly allow AI coding tools; require completed DESIGN.md, EVALS.md and AI_BUILD_LOG.md, at least 30 authored evals, a commit SHA and a ten-minute demo.

## Candidate starts

```sh
cd northstar-candidate
docker compose up --build -d
docker compose run --rm public-evals
```

The safe starter deliberately fails most task examples until implemented. Its web demo is http://localhost:8000. README also has Python-only instructions.

## Hiring team grades privately

```sh
cd northstar-evaluator
python setup_local.py
docker build -t northstar-submission:local ../northstar-candidate
docker compose up --build -d mock-api candidate-agent
docker compose run --rm grader python run_assessment.py --agent-url http://candidate-agent:8000 --api-url http://mock-api:8001 --candidate-id FDE-017 --trials 3 --report-dir /reports/FDE-017
docker compose down
```

Replace the build path with the actual submitted repository at its exact commit. Add budget-limited model credentials only to .candidate.env. Read reports/FDE-017/report.md and the server-side traces privately, complete the human rubric, then choose one 45-minute phase-2 card. Candidates never receive hidden cases, grader files or answer traces. Automatic scoring is 60 points; 40 evidence-backed human points remain pending until review.

To validate the evaluator without Docker or model access: `python run_assessment.py --self-check --trials 3` from its root. For detailed commands, scores, limitations and live acceptance packs, read its README. See [verification/VERIFICATION.md](verification/VERIFICATION.md) for the actual validation performed on this delivery.
