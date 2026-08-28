# Recoverability Is Not Recognition

> A frozen-language-model study of test-time capability extraction, hidden-state diagnosis, and the limits of inference-time selection.

**[Read the research site](https://samat2003.github.io/capability-research/)** · **[Read audited results](RESULTS.md)** · **[Read the manuscript](paper/main.tex)** · **[Reproduce the public audit](docs/REPRODUCIBILITY.md)**

This repository is the cleaned publication artifact for a sequential study of frozen-language-model inference. It asks: when a pretrained language model can generate a correct solution under sampling, how much of the remaining behavioral gap is caused by selecting that solution rather than by its absence from the sampled candidate bank?

The study uses frozen `Qwen/Qwen2.5-7B` and `Qwen/Qwen2.5-7B-Instruct` backbones. The central decomposition is

\[
E_k(x)=\mathbf 1\{\text{at least one of the first }k\text{ samples is correct}\},
\qquad
R_X=P(S_X=1\mid E_k=1),
\]

so an inference system can fail because the correct behavior is not recoverable from its candidate bank, or because the system fails to recognize a correct candidate that is already present.

## Main findings

1. **Internal mechanically verified tasks:** multi-sample recoverability can be much larger than one-shot Base accuracy. A high-compute frozen selector (historical X5) reached 61.75% on a 400-task internal distribution versus 45.75% for one-sample Qwen2.5-7B-Instruct, but this comparison used substantially more inference compute for Base and is not an equal-compute superiority claim.
2. **Recognition is a distinct bottleneck:** later experiments found near-oracle candidate coverage without reliable final selection, and single-pass spectral steering failed causal controls.
3. **Correctness is represented internally:** an all-layer calibration atlas found strong task-dependent hidden-state signal. For Base, the best fixed representation achieved 54.69% calibration selection accuracy while a task-specific representation oracle reached 71.88%, leaving 17.19 percentage points of diagnostic headroom.
4. **Adaptive readout did not solve recognition:** nearest-experience routing and a learned 43,649-parameter representation router both failed preregistered held-out gates.
5. **Public HumanEval+ transfer was negative:** on all 164 HumanEval+ tasks, ordered Base recoverability was 8/164 at k=1 and 30/164 at k=8, while Instruct was 119/164 and 132/164. Base MetaAtlas selected 11/164 from the 8-sample bank; its preregistered comparisons against sample 0 and the strongest fixed readout were not decisive.

The public coding result is important because it **does not** reproduce the internal convergence of Base and Instruct recoverability with larger k. The probability-concentration interpretation is therefore distribution-specific: on HumanEval+, post-training is associated with a large matched-k recoverability advantage, not merely better selection among an equivalent Base pool.

## Statistical correction

The original v0.4.0 audit incorrectly reported unbiased pass@1/pass@2/pass@4 by counting successes only inside the ordered k-prefix and then applying the n=8 Codex estimator. The estimator requires the total number of successful samples in the complete 8-sample bank. Those three values are withdrawn here. **Ordered empirical recoverability E_k, selected@8 results, paired bootstrap intervals, exact McNemar tests, and pass@8 are unaffected.** See [`docs/STATISTICAL_CORRECTION.md`](docs/STATISTICAL_CORRECTION.md).

## Repository layout

- [`RESULTS.md`](RESULTS.md) — audited project-level results and claim boundaries.
- [`paper/main.tex`](paper/main.tex) — full manuscript.
- [`docs/RESEARCH_TIMELINE.md`](docs/RESEARCH_TIMELINE.md) — mapping from historical X5–X9 labels to scientific questions.
- [`docs/AUDIT.md`](docs/AUDIT.md) — code/statistics/provenance audit.
- [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) — reproduction protocol and source commit provenance.
- [`configs/`](configs/) — cleaned frozen protocol summaries.
- [`results/`](results/) — compact audited aggregate results.
- [`src/capability_research/`](src/capability_research/) — corrected metric and audit utilities.
- [`tests/`](tests/) — tests for the recoverability/pass@k distinction.
- [`docs/index.html`](docs/index.html) — source for the GitHub Pages research site.
- [`docs/BRANCH_RECONCILIATION.md`](docs/BRANCH_RECONCILIATION.md) — how every historical `meta-cognition` branch maps into the canonical publication record.

## Claim boundary

This work does **not** establish a universal replacement for SFT/RL, universal Base/Instruct capability parity, a general hidden-state verifier, or state-of-the-art coding performance. Its strongest contribution is a reproducible decomposition and a sequence of positive and negative mechanistic tests showing that **recoverability, diagnostic correctness signal, and reliable behavioral recognition are different properties**.

## Provenance

The final source experiment was preregistered at source commit `bbdad096d67d39a8564ba4eb1f9fab474e384728` and reported at source commit `645e89d2846930c74d3f8e85e5a25e6ec1abefdb`. This repository is intentionally a clean publication artifact rather than a copy of the historical development Git history.

## Publication checklist

1. Push this repository's `main` branch to GitHub.
2. In **Settings → Pages**, select **GitHub Actions** as the source. The included workflow deploys `docs/` to `https://samat2003.github.io/capability-research/`.
3. Confirm the site URL and repository metadata render correctly, then add the final PDF or archival DOI if one becomes available.

The manuscript draft remains the scientific source of record. Do not replace the withdrawn HumanEval+ unbiased pass@1/pass@2/pass@4 values without the complete candidate-outcome files and an exact recomputation.
