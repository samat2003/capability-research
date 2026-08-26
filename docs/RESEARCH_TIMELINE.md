# Research timeline

The historical X-labels were development identifiers. This publication uses them only to preserve provenance while organizing the work by scientific question.

| Historical label | Scientific question | Outcome | Main lesson |
|---|---|---|---|
| X5 | Can a frozen Base model outperform a one-sample Instruct comparator with large test-time search and recognition compute? | Positive on a 400-task internal set | Search plus recognition can expose substantial frozen capability, but the comparison used much more inference compute for Base. |
| X6 | If the correct candidate is preserved in a shortlist, is recognition solved? | Negative | Candidate coverage and final recognition are distinct bottlenecks. |
| X7 | Can unsupervised spectral hidden-state geometry provide a useful single-pass causal steering direction? | Negative | Diagnostic-looking geometry does not imply a useful control direction. |
| X8 / Metacognitive Atlas | Is correctness signal task-dependent across layer/time views, and can nearest-experience routing exploit it? | Mixed/negative | Large diagnostic view headroom exists, but the non-parametric router failed against the strongest fixed view. |
| X9 / MetaRoute | Can a small learned router predict which representation should be trusted on a new task? | Negative | Weak utility prediction did not recover the task-specific view oracle gap; direct correctness supervision was stronger internally. |
| Public HumanEval+ transfer | Do the strongest frozen recognition mechanisms transfer unchanged to public coding? | Negative / not decisive | MetaAtlas did not decisively beat sample0 or best-fixed; Base matched-k recoverability remained far below Instruct. |

## Why the sequence matters

The project progressively separated three propositions that are easy to conflate:

1. **Existence:** a correct trajectory can appear somewhere in the frozen model's sampling distribution.
2. **Diagnosis:** internal representations can contain information correlated with whether a trajectory is correct.
3. **Control:** a deployable inference mechanism can reliably use that information to select or cause the correct behavior.

The experiments provide evidence for the first two on the tested internal distributions. They do not establish the third as a general mechanism.

## Development versus confirmation

The overall X-series is a sequential research program rather than a single preregistered study. Individual later stages used frozen gates and untouched confirmation sets. Failed gates stopped confirmation for X8 and X9. The final HumanEval+ protocol was committed before public model generation and was run as a single external transfer evaluation.

This distinction is important when interpreting the evidence: exploratory development motivates mechanisms; held-out gates and the public transfer determine whether those mechanisms generalized.
