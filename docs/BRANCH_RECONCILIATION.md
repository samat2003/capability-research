# Historical branch reconciliation

This publication artifact reconciles the complete `samat2003/meta-cognition` branch history as of the final HumanEval+ result. Historical branches are preserved as provenance, not copied wholesale: they contain evolving code, intermediate reports, and superseded framing. The tables and source commits below define the canonical publication record.

| Historical branch | Canonical role | Publication treatment |
|---|---|---|
| `master` | Pre-X5 measurement and audit history | Context only. Earlier flawed v0.3 artifacts remain forensic records and are not used for claims. |
| `v035-metacognitive-controller` | X5 frozen high-compute selection | Retain the 400-task internal result and its unequal-compute boundary. |
| `v036-explore-converge` | X6 coverage-versus-recognition gate | Retain as a failed frozen gate. Near-oracle shortlist coverage did not yield reliable selection. |
| `v037-spectra-single-pass` | X7 single-pass causal control | Retain as a negative causal-control result, including proper, delayed, and opposite-direction controls. |
| `v038-metacognitive-atlas` | X8 protocol freeze | Use only with the audited result below; do not promote pre-result design material to outcome evidence. |
| `v038-metacognitive-atlas-agent` | X8 audited atlas result | Retain task-dependent diagnostic headroom and the failed best-fixed gate. |
| `v039-learned-metarouter` | X9 learned representation router | Retain as a failed preregistered gate; the 43,649-parameter router did not recover the task-specific-view oracle gap. |
| `v040-humanevalplus-final` | Final public transfer | Retain ordered recoverability and selected@8 results. Withdraw archived unbiased pass@1/pass@2/pass@4 values because of the prefix-count error. |

## Canonical terminology

- **Ordered recoverability, E_k:** at least one correct program occurs among the ordered first `k` candidates in a fixed bank.
- **Conditional recognition:** selection accuracy conditional on a correct candidate being present.
- **selected@8:** accuracy after an inference procedure chooses one candidate from an eight-candidate bank; it is not ordinary leaderboard pass@1.
- **Unbiased pass@k:** the standard subset-sampling estimator using the total number of successes in the full `n`-sample bank. It is not ordered recoverability.

The canonical claims, figures, and statistics are in [RESULTS.md](../RESULTS.md), [the manuscript](../paper/main.tex), and [the claim matrix](CLAIM_MATRIX.md). These files supersede branch-local “state of the art” labels and any wording that implies general benchmark leadership or universal Base/Instruct equivalence.

## Final evidence boundary

The project supports a decomposition: recoverable capability, diagnostic correctness signal, and reliable behavioral recognition are distinct properties. It does not establish a general frozen-model control method, a substitute for post-training, or state-of-the-art public code-generation performance. The public HumanEval+ transfer is retained precisely because it narrows the internal interpretation.
