# Audited Results

## Research question

The experiments separate two failure modes for a frozen language model:

- **recoverability**: whether at least one correct candidate appears in an ordered sample bank;
- **recognition**: whether an inference-time selector chooses a correct candidate when one is available.

For model \(M\), task \(x\), and prefix size \(k\),

\[
E_{M,k}(x)=\mathbf 1\{\exists j\le k:\tau_j\text{ is correct}\}.
\]

For selector \(X\), conditional recognition is

\[
R_X(k)=P(S_X=1\mid E_k=1).
\]

The experiments use frozen Qwen2.5-7B Base and Qwen2.5-7B-Instruct backbones in BF16 without quantization.

---

## 1. High-compute frozen selection (historical X5)

On a fresh 400-task mechanically verified internal reasoning set:

| System | Accuracy |
|---|---:|
| Base, one sample | 103/400 = 25.75% |
| Instruct, one sample | 183/400 = 45.75% |
| Frozen Base + X5 selector | 247/400 = 61.75% |
| Base pool oracle, k=32 | 391/400 = 97.75% |

X5 minus one-sample Instruct was **+16.0 percentage points**, paired task-bootstrap 95% CI **[+10.25,+21.75] pp**, exact McNemar **p=1.446e-7**.

**Critical caveat:** this was not an equal-compute comparison. X5 used 32 Base candidates plus representation replay, pairwise comparisons, and self-verification; the Instruct comparator used one completion. The result shows that frozen test-time inference can expose substantial capability on this distribution, not that Base is generally superior to post-training.

---

## 2. Coverage without recognition (historical X6)

On a fresh 100-task mechanistic gate:

| System | Accuracy |
|---|---:|
| Base | 26% |
| Instruct | 48% |
| same-pool X5 | 66% |
| X6 | 62% |
| X6 shortlist oracle | 97% |
| Base E32 | 97% |

The correct answer survived X6's shortlist almost whenever it existed, but final recognition remained weak. On constraint tasks, a correct candidate was retained on 22/25 tasks while X6 selected correctly only 1/25.

A separate 80-task applied gate was capability-limited for Base: Instruct scored 61/80=76.25%, while the entire Base k=32 pool oracle was 59/80=73.75%. No selector restricted to that sampled Base pool could beat Instruct overall.

---

## 3. Diagnostic geometry is not automatically causal control (historical X7)

A strict single-trajectory spectral steering rule was tested on 160 fresh tasks:

| Arm | Accuracy |
|---|---:|
| Base | 44/160 = 27.50% |
| X7 spectral steering | 38/160 = 23.75% |
| delayed control | 41/160 = 25.63% |
| opposite direction | 38/160 = 23.75% |
| Instruct | 94/160 = 58.75% |

Proper and opposite steering had identical aggregate accuracy. This experiment provides no evidence that the unsupervised spectral direction was a useful causal control direction.

---

## 4. Metacognitive Atlas (historical X8)

### Calibration representation headroom

For Base, the strongest fixed hidden-state view reached **54.69%** cross-validated task-level selection accuracy at k=8. A diagnostic task-specific view oracle reached **71.88%**, leaving **+17.19 pp** of representation-selection headroom.

For Instruct, the corresponding values were **71.09%** fixed and **78.91%** oracle, a **+7.81 pp** gap.

This supports the claim that correctness-related signal can vary materially across layer/time representations. The oracle is diagnostic only and is not a deployable selector.

### Frozen 96-task gate

Base at k=8:

| Arm | Accuracy |
|---|---:|
| sample 0 | 21/96 = 21.88% |
| self-consistency | 32/96 = 33.33% |
| best fixed view | 48/96 = 50.00% |
| MetaAtlas | 46/96 = 47.92% |
| pool recoverability E8 | 65/96 = 67.71% |

MetaAtlas beat self-consistency by **+14.58 pp**, 95% CI **[+4.17,+25.00]**, McNemar **p=.01254**, but was below the preregistered best-fixed baseline by **-2.08 pp**, 95% CI **[-11.46,+7.29]**, **p=.8238**. The gate failed and confirmation did not run.

Matched ordered recoverability:

| k | Base E_k | Instruct E_k |
|---:|---:|---:|
| 1 | 21.88% | 48.96% |
| 2 | 41.67% | 58.33% |
| 4 | 50.00% | 65.63% |
| 8 | 67.71% | 75.00% |
| 16 | 75.00% | 78.13% |
| 32 | 79.17% | 85.42% |

The large k=1 gap contracted strongly by k=32, which is consistent with an important probability-concentration component on this internal distribution, while the remaining 6.25 pp E32 gap prevents an equal-recoverability claim.

---

## 5. Learned representation routing (historical X9 / MetaRoute)

A 43,649-parameter shared MLP was trained to predict fold-excluded representation utility rather than candidate correctness. On the frozen 160-task Base gate at k=8:

| Arm | Accuracy |
|---|---:|
| sample 0 | 36/160 = 22.50% |
| self-consistency | 56/160 = 35.00% |
| best fixed | 72/160 = 45.00% |
| global learned view weights | 61/160 = 38.13% |
| MetaAtlas | 95/160 = 59.38% |
| MetaRoute | 75/160 = 46.88% |
| direct learned verifier | 84/160 = 52.50% |
| task-specific view oracle | 117/160 = 73.13% |

MetaRoute exceeded best-fixed pointwise by +1.875 pp but not decisively (95% CI [-3.75,+7.50]). It exceeded global learned weights by +8.75 pp (CI [+2.50,+15.00]) but was **12.50 pp below MetaAtlas** (CI [-19.375,-5.625]). The preregistered gate failed; confirmation did not run.

The view oracle minus best-fixed gap was 28.13 pp on this gate, yet MetaRoute captured only about 6.7% of that gap. Predicted utility correlated weakly with realized utility (Base Spearman 0.202) and Top-4 oracle-view recall was 21.74%.

Matched recoverability again converged internally:

| k | Base E_k | Instruct E_k |
|---:|---:|---:|
| 1 | 22.50% | 49.38% |
| 2 | 37.50% | 61.88% |
| 4 | 55.63% | 72.50% |
| 8 | 73.13% | 81.25% |
| 16 | 82.50% | 84.38% |
| 32 | 88.75% | 88.13% |

---

## 6. Final public transfer: HumanEval+

The final evaluation used EvalPlus 0.3.1, HumanEval+ v0.1.10, all 164 tasks, and immutable eight-sample banks for both Base and Instruct. The public protocol was frozen before model generation.

### Ordered recoverability

| k | Base E_k | Instruct E_k |
|---:|---:|---:|
| 1 | 8/164 = 4.88% | 119/164 = 72.56% |
| 2 | 13/164 = 7.93% | 128/164 = 78.05% |
| 4 | 21/164 = 12.80% | 130/164 = 79.27% |
| 8 | 30/164 = 18.29% | 132/164 = 80.49% |

Unlike the internal studies, the Base/Instruct recoverability gap remained very large at k=8: **-62.20 pp** for Base minus Instruct. The internal probability-concentration pattern therefore did **not** transfer to this public coding benchmark.

### Base selection from the eight-sample bank

| Selector | selected@8 |
|---|---:|
| sample 0 | 8/164 = 4.88% |
| best fixed | 9/164 = 5.49% |
| MetaAtlas | 11/164 = 6.71% |
| MetaRoute | 12/164 = 7.32% |
| direct verifier | 6/164 = 3.66% |
| pool oracle | 30/164 = 18.29% |

Preregistered MetaAtlas comparisons:

- vs sample 0: **+1.83 pp**, bootstrap 95% CI **[-1.83,+6.10]**, exact McNemar **p=.5488**, discordant cells 7/4.
- vs best fixed: **+1.22 pp**, bootstrap 95% CI **[-3.05,+5.49]**, exact McNemar **p=.7744**, discordant cells 7/5.

Neither primary public comparison was decisive. MetaRoute was numerically 1/164 above MetaAtlas but was an unchanged mechanism that had already failed its internal gate; this single external observation does not rehabilitate the routing hypothesis.

### Instruct selection context

At k=8, Instruct sample 0 was 119/164=72.56%, self-consistency 122/164=74.39%, MetaAtlas 117/164=71.34%, MetaRoute 114/164=69.51%, and pool oracle 132/164=80.49%.

### Correction to the original public audit

The original v0.4.0 report's unbiased pass@1/pass@2/pass@4 values are invalid because the audit used the number of successes in the first k ordered samples as \(c\) while setting \(n=8\). The standard Codex estimator requires \(c\) to be counted over all n=8 samples. The publication artifact therefore withdraws those values rather than silently substituting new ones. pass@8 equals empirical E8 and is unaffected.

---

## Final scientific conclusion

The strongest supported conclusion is not a universal alignment mechanism but a decomposition:

> **Recoverable capability, diagnostic correctness information, and reliable behavioral recognition are distinct.** Sampling can reveal correct behavior that one-shot decoding misses, and hidden states can contain correctness-related signal, but the tested causal steering, non-parametric adaptive readout, and learned representation-routing methods did not consistently convert that signal into reliable held-out selection.

The matched-k comparison is distribution-dependent. Internal tasks showed strong Base/Instruct convergence with sampling; HumanEval+ did not. Therefore the data do not support a universal claim that post-training merely concentrates probability over an unchanged capability set.

No generic state-of-the-art performance claim is made.
