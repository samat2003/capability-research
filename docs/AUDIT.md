# Independent audit of the final research artifact

This document records a repository-level audit of the archived experiment source before creating this clean publication repository.

## Source commits checked

- Final HumanEval+ result: `645e89d2846930c74d3f8e85e5a25e6ec1abefdb`
- Pre-evaluation freeze: `bbdad096d67d39a8564ba4eb1f9fab474e384728`
- Public-evaluation implementation immediately preceding the freeze: `f46b5b504e6ccb56597b86ab72f56057d7c9bff3`
- Starting audited X9 result: `ab1b978c12ef713a70ec7afc4a1746cd9ed21020`

The pre-evaluation commit contains a frozen declaration that no HumanEval+ model completion is generated until after that commit is pushed. The immediately preceding implementation commit contains the generation, replay, selection, evaluator, preflight, and machine-readable protocol.

## Public protocol verified

The frozen configuration specifies:

- EvalPlus 0.3.1, HumanEval+ v0.1.10, all 164 tasks;
- Qwen2.5-7B Base revision `d149729398750b98c0af14eb82c78cfe92750796`;
- Qwen2.5-7B-Instruct revision `a09a35458c702b33eeacc393d103063234e8bc28`;
- BF16, no quantization, no backbone weight changes;
- one immutable bank of 8 samples/model/task;
- nested ordered prefixes k={1,2,4,8};
- temperature 0.8, top-p 0.95, maximum 384 generated tokens;
- selector checkpoints/hashes inherited from the prior X9 development stage;
- no HumanEval selector training and no post-freeze tuning.

The committed generation metadata records exactly 164 tasks and 1,312 candidates per model. The actual resolved model revisions in generation metadata match the revisions written into the frozen protocol.

## Selection/evaluation separation

The implementation is staged:

1. generate candidate ledgers;
2. replay hidden representations;
3. compute selector choices and write hashed selection manifests;
4. execute EvalPlus;
5. attach `plus_status` outcomes to candidates and selections;
6. recompute aggregate statistics.

`v040_transfer.py` computes selector scores from representations, unlabeled candidate-bank features, and frozen calibration artifacts. It does not consume candidate correctness or EvalPlus outcome fields. `v040_eval.py` reads the already-written selection manifest and then attaches official EvalPlus outcomes.

### Qualification

The archived orchestration module imports `evalplus.data` and obtains the complete HumanEval+ task objects before stripping them to `task_id`, `prompt`, and `entry_point`. Therefore an old statement that the first stages “do not import EvalPlus tests” is too strong. The stronger supported statement is:

> **The selector functions receive only public prompt/entry-point data and label-free representations; benchmark tests and execution outcomes are not passed into selector computation.**

The clean paper uses this wording.

### Temporal-proof limitation

The source repository preregisters the protocol before generation, and the runtime workflow records hashes for selection manifests before evaluator invocation. However, the actual selection manifests and evaluator outputs were pushed together in the final result commit. GitHub therefore does not provide an independent external timestamp proving that a particular manifest existed before evaluation. The evidence for ordering is the staged code, local stage metadata, hashes, and reported execution procedure—not a separately pushed pre-evaluation selection commit.

This is treated as a reproducibility limitation, not as proof of leakage.

## Candidate-bank and replay integrity

The archived audit reports:

- exact 0..7 sample indices for the public bank;
- 1,312 candidates per model;
- recorded exact prompt token IDs and completion token IDs;
- label-free held-out representation archives;
- selection hashes tied to candidate trajectory hashes;
- independent recomputation from candidate outcomes and frozen selections.

The final generation metadata reports zero security-redaction events in generated raw text for the public run.

## Statistical audit

### Valid

The following public metrics are internally consistent with the committed per-task result summary and audit code:

- ordered recoverability E1/E2/E4/E8;
- selected@8 arm accuracies;
- conditional recognition at k=8;
- oracle-gap closure at k=8;
- paired task bootstrap confidence intervals;
- exact two-sided McNemar tests and discordant counts;
- Base/Instruct E_k differences;
- pool oracle E8.

The exact McNemar implementation uses a two-sided binomial test over the discordant pairs, which is appropriate for the reported paired binary comparisons.

### Corrected

The archived `v040_audit.py` contains a pass@k aggregation bug. For each k it truncates a task's eight outcomes to the ordered first-k prefix, counts successes in that prefix, and then calls the standard estimator with `n=8`. The standard estimator requires the number of successes across all eight samples. Consequently the archived unbiased pass@1/pass@2/pass@4 values are invalid. pass@8 is unaffected.

See `STATISTICAL_CORRECTION.md` and the corrected implementation in this repository.

## Reproducibility weaknesses corrected in the clean artifact

1. **Model revision enforcement.** The archived frozen protocol records exact model revisions and the run resolved to those revisions, but the generation code loaded the model/tokenizer by repository name without explicitly passing the frozen revision. The clean protocol treats the recorded revision as mandatory for future reproduction.
2. **Sample ordering in audit.** The archived post-hoc audit relied on CSV row order when reconstructing each task's candidate bank. The clean audit code explicitly sorts by `sample_index`.
3. **Local code execution.** The archived HumanEval+ run used EvalPlus's official local evaluator because Docker was unavailable to that account. EvalPlus documents local execution as less safe than containerized execution. Future reproduction should use the official containerized evaluator or an equivalently isolated sandbox.
4. **Development-repository clutter.** Historical runbooks, agent instructions, temporary logs, version-specific notes, and operational files are intentionally excluded from this publication repository.
5. **Raw generated text.** This clean repository does not republish model-generated raw text. Aggregate outcome tables, protocol provenance, and corrected analysis code are sufficient for the claims made here and avoid unnecessary exposure of incidental generated content.

## Security audit of the clean repository

The clean repository is constructed from new publication files rather than copied Git history. It contains no machine-access commands, private-key material, host addresses, local workstation paths, authentication tokens, model caches, or operational agent transcripts.

## Audit verdict

The central scientific result survives audit with a narrower and cleaner claim:

- internal experiments provide strong evidence that one-shot behavior can understate sampled recoverability and that hidden states carry correctness-related signal;
- the tested recognition/control mechanisms fail to establish general held-out control;
- the final HumanEval+ run provides no decisive evidence of selector transfer and strongly contradicts a universal Base/Instruct recoverability-convergence claim;
- one secondary metric family (unbiased pass@1/2/4 in the archived public report) must be withdrawn due to an aggregation bug.

This is a valid mechanistic/negative-results research contribution, not a state-of-the-art benchmark-performance result.
