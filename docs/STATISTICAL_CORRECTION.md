# Statistical correction: HumanEval+ pass@k

## Scope

This note corrects one metric family in the archived v0.4.0 HumanEval+ audit. It does **not** change the candidate outcomes, ordered recoverability curves, selected@8 accuracies, bootstrap confidence intervals, exact McNemar tests, or the scientific conclusion.

## The bug

For a bank of `n=8` generated candidates with `c` correct candidates, the standard unbiased Codex estimator is

\[
\widehat{\mathrm{pass@}k}=1-\frac{\binom{n-c}{k}}{\binom{n}{k}}.
\]

The archived audit correctly implemented this function, but called it with an incorrect value of `c` for k<8. The code first truncated each task's ordered bank to `v[:k]`, counted successes in that prefix, and then called `pass_at_k(8, c_prefix, k)`.

That is inconsistent with the estimator: `c` must count correct samples across the **entire n=8 bank**, regardless of the k being estimated.

In pseudocode, the archived pattern was:

```python
prefix = successes[:k]
c = sum(prefix)                 # incorrect input for unbiased pass@k
pass_at_k(n=8, c=c, k=k)
```

The corrected pattern is:

```python
c_total = sum(successes)        # all 8 candidates
pass_at_k(n=8, c=c_total, k=k)
```

## Why the error is detectable from aggregate results

Base ordered recoverability at k=8 was 30/164. Therefore at least 30 of the 1,312 Base candidates were correct. Any valid unbiased pass@1 estimate from the eight-sample bank must therefore be at least

\[
30/(164\times8)\approx2.29\%.
\]

The archived report gave 0.61%, which is impossible under the same candidate outcomes. Likewise, Instruct E8=132/164 implies at least 132 correct candidates among 1,312, so a reported 9.07% pass@1 is below the minimum possible 10.06%.

## Publication policy

The clean publication artifact:

- withdraws the archived unbiased pass@1/pass@2/pass@4 numbers;
- retains ordered empirical recoverability E1/E2/E4/E8;
- retains selected@8 results and paired tests;
- retains pass@8, which is equal to E8 when k=n=8 and was unaffected by the prefix-count error;
- provides corrected recomputation code in `src/capability_research/metrics.py` and `src/capability_research/public_audit.py`.

We do not infer replacement pass@1/pass@2/pass@4 values from summary statistics alone. Exact recomputation requires the complete candidate-outcome file.

## Scientific impact

None of the primary public hypotheses depended on unbiased pass@k. Both primary tests compared the preselected MetaAtlas output against sample 0 and the strongest fixed readout on the same 164 tasks. Those paired outcomes and tests are unaffected.

The final public conclusion remains negative: the tested hidden-state selector did not show decisive transfer, and Base matched-k recoverability remained far below Instruct on HumanEval+.
