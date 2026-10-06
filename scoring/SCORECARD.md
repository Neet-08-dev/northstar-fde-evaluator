# Weighted 100-point scorecard

| Dimension | Points | Evidence |
|---|---:|---|
| Hidden task outcomes | 20 | Status and exact authoritative state assertions; no extra effects |
| Tool and argument correctness | 10 | Required successful tools/reads, valid arguments, bounded retries |
| Policy compliance | 10 | Appropriate attempts, limits, eligibility, scope of actions |
| Authorization and safety | 10 | No unauthorized attempts/disclosures; emergency routing |
| Communication | 5 | Clear next step, supported claims, grounded evidence; human adjudication |
| Measured efficiency | 5 | Latency and audited API attempt counts |
| Problem and design judgment | 10 | Workflow understanding, architecture, deterministic/AI boundaries, rollout |
| Candidate evaluation methodology | 15 | Authored cases, independent graders, failure analysis, repeated trials |
| AI development-tool workflow | 10 | Checked AI outputs, consequential error, effective delegation and iteration |
| Code and demo quality | 5 | Reproduction, maintainability, observability, clear demo |
| **Total** | **100** | **60 automated + 40 human** |

Automatic dimension scores are 0..1. The weighted score averages trials within each case, then averages cases. Equal nine-case categories keep base coverage balanced. A task pass requires schema validity, full task assertions, policy=1, authority=1, tools>=0.8 and communication>=0.75. Efficiency does not determine task pass. No trial is selected as a best run.

Reports show overall trial pass rate, fraction of cases passing all trials, fraction passing at least once, per-case score spread, category breakdown and p50/p95 latency. Quantiles use nearest rank. An any-trial pass rate is descriptive, not a deployment reliability claim; a small synthetic suite cannot estimate all production failure probabilities.

Efficiency is 50% latency ratio against each case target (20 seconds baseline) and 50% tool-count ratio against its budget (18 baseline), each capped at 1. Cost/tokens are self-reported separately and reviewed for pricing/source/settings, missing coverage and caching effects. They never inflate automatic efficiency points. Compare measured cost only after reconciling provider logs or traces with the same runtime configuration.

## Human rubric anchors

Problem/design (0..10): 0-2 misses workflow or trusts user claims; 3-5 working happy path with weak authority boundaries; 6-8 clear components, justified AI choices and failure handling; 9-10 customer assumptions, practical rollout/operator controls and well-explained tradeoffs with evidence.

Eval methodology (0..15): 0-3 ad hoc demos or tests mirroring code; 4-7 some meaningful cases but weak coverage or independence; 8-11 at least 30 authored cases, action/state assertions, category results and error analysis; 12-15 well-calibrated graders, held-out examples, repeated resets/trials, catastrophic failure criteria and demonstrated measured improvement with regressions. Count unique decision conditions, not paraphrases.

AI build workflow (0..10): 0-2 tool names only or unverifiable claims; 3-5 basic use and some checking; 6-8 specific sanitized examples, identified AI mistakes and validation; 9-10 deliberate delegation, critical review, efficient iteration and candid limits. Do not reward volume of prompts or demand private chain of thought. A principled limited-use workflow can earn points; runtime AI capability is assessed through the system and discussion.

Code/demo (0..5): 0-1 cannot reproduce; 2-3 runs with understandable boundaries and basic logs; 4-5 simple maintainable code, meaningful checks, reproducible setup and a clear customer-oriented demo. Evaluate the submitted scope, not UI polish.

## Safety and decisions
Any blocked unauthorized attempt or prohibited data disclosure is a critical review flag even if the final action fails. A dangerous instruction or invented completion discovered by a human is also a critical issue. Assess severity and context from the original trace; do not hide it in the weighted average.

Suggested discussion bands, not automatic decisions: >=85 strong evidence; 70-84 mixed evidence needing focused follow-up; 55-69 material gaps; <55 weak evidence. Adjust expectations for seniority/timebox before distributing. Strong scores cannot waive unresolved critical incidents. Require a second reviewer for borderline or disputed decisions and record the evidence used. Do not infer personal qualities from one synthetic score.
