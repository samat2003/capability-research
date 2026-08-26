# Claim matrix

This table separates observations directly supported by the experiments from interpretations that remain conditional.

| Claim | Status | Evidence boundary |
|---|---|---|
| One-shot Base accuracy can substantially understate multi-sample recoverability. | **Supported internally** | Repeated across mechanically verified internal task sets; magnitude is distribution- and budget-specific. |
| A frozen high-compute inference system can outperform the specified one-sample Qwen2.5-7B-Instruct comparator. | **Supported on X5 internal distribution** | Unequal inference compute; not a Base-vs-Instruct model-quality claim. |
| Candidate coverage and final recognition are distinct bottlenecks. | **Supported** | X6 preserved correct candidates near the pool oracle while final selection remained substantially weaker. |
| Hidden-state representations contain correctness-related diagnostic information. | **Supported on tested internal tasks** | All-layer atlas and related candidate-level analyses; does not imply causal controllability. |
| The best diagnostic readout can vary by task across depth/time. | **Supported diagnostically** | Large fixed-vs-task-oracle gaps in X8/X9; oracle readout is not deployable. |
| Unsupervised spectral geometry provides a useful one-shot causal control direction. | **Not supported** | X7 proper/opposite/delayed controls failed. |
| Nearest-experience adaptive representation routing reliably beats a strong fixed readout. | **Not supported** | X8 frozen gate failed. |
| Learned task-conditioned representation routing reliably closes the adaptive-view oracle gap. | **Not supported** | X9 frozen gate failed; routing-headroom capture was small. |
| MetaAtlas transfers as a general public-code selector. | **Not supported by HumanEval+** | Both preregistered paired comparisons were inconclusive and small. |
| Post-training only concentrates probability over capabilities already recoverable from Base. | **Rejected as a universal interpretation** | Internal matched-k gaps sometimes converge, but HumanEval+ Base E8=18.29% versus Instruct E8=80.49%. |
| Frozen inference can generally replace SFT/RL. | **Not established** | No experiment supports a universal replacement claim. |
| The project establishes benchmark state of the art. | **No** | Private internal tasks and low public HumanEval+ selected@8 scores; inference protocols are not comparable to standard leaderboard pass@1. |

## Short final hypothesis

The research most strongly supports the following hypothesis:

> **Recoverable capability, diagnostic correctness information, and reliable behavioral recognition are separate properties of a language-model inference system.**

A useful engineering consequence follows: measure recoverability before deciding whether a failure calls primarily for additional training/capacity or for better inference-time verification and search.
