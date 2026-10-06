# Interviewer guide

## Before distribution
Use one candidate repository, policy version, timebox and model budget for everyone in the round. Recommended: a compensated six-hour take-home, two optional hours of polish, a ten-minute demo and a 45-minute live change. Ask candidates about access and accommodations; provide model access or an equivalent local option. Give the published score dimensions and an honest description of remaining work in the starter. Never expose the evaluator repository, traces or case names.

## Before the interview
Record candidate commit, image digest, model/provider settings and start instructions. Run their own evals separately, then the hidden suite with three fresh trials each. Review safety flags first and inspect two ordinary successes, two failures and one inconsistent case. Compare their evaluation claims against actual action evidence. Do not equate lack of hidden coverage with dishonesty; their dataset may sample a different distribution.

Spend 15 minutes reading DESIGN.md, EVALS.md and AI_BUILD_LOG.md. Choose the phase-2 request before the live session, using the same request for candidates at the same level unless an accommodation requires otherwise. The live API contract, policy change and acceptance criteria must be shown at the start; do not make the exercise a surprise schema guessing game.

## Suggested 75-minute conversation
0-10: candidate demo (one completed task, one clarification, one safety case).
10-20: design and eval discussion.
20-65: one 45-minute live change with AI coding tools allowed.
65-75: review results, unresolved tradeoffs and candidate questions.

Useful questions: What would the operations manager count as a successful resolution? Which AI step could you replace with deterministic code? Show a case your own grader marked successful incorrectly. How do you know a credit actually committed? What changes after a lost response? How did you catch the largest AI-generated mistake? What would you log without leaking customer data? What data would you collect in a shadow deployment? Where would a human be in the loop?

For nondeterministic failures, ask for a hypothesis and a discriminating test. Do not ask for private thought processes or reward someone for reciting a model framework. Observe whether the candidate checks evidence, scopes changes, updates evals, communicates tradeoffs and recovers from mistakes.

## During phase 2
Allow five minutes to inspect and plan, about 30 to implement and test, and ten to demonstrate/regress. Provide the candidate-facing card, current policy/fixture input and acceptance criteria. Keep answer traces and private tests to yourself. Candidate tools are permitted. The test is engineering judgment under a changing customer requirement, not typing speed.

## Afterward
Enter points with specific files, traces or examples in the human review template. Adjudicate communication heuristics when reasonable alternate language was incorrectly penalized. Add human safety observations. Compare within the agreed timebox and budget, have a second reviewer examine disputes, and write a concise evidence-based rationale. Share general feedback, not hidden cases, while the suite remains in use. Rotate cases between rounds if they leak.
