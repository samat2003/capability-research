# Reproducibility

## Public transfer provenance

The final public evaluation is anchored to the following archived source commits:

- X9 audited starting point: `ab1b978c12ef713a70ec7afc4a1746cd9ed21020`
- HumanEval+ implementation commit: `f46b5b504e6ccb56597b86ab72f56057d7c9bff3`
- pre-evaluation frozen protocol: `bbdad096d67d39a8564ba4eb1f9fab474e384728`
- final HumanEval+ result: `645e89d2846930c74d3f8e85e5a25e6ec1abefdb`

This clean repository intentionally does not copy the development Git history.

## Recorded environment

The archived public run recorded:

```text
Python       3.10.12
PyTorch      2.13.0+cu130
Transformers 5.16.1
vLLM         0.28.0
EvalPlus     0.3.1
GPU          NVIDIA A100-SXM4-40GB
```

The original public benchmark generated 2,624 trajectories in total: 164 tasks x 8 candidates x 2 models.

## Model revisions

Reproduction should pin exact revisions rather than only repository names:

```text
Qwen/Qwen2.5-7B
revision d149729398750b98c0af14eb82c78cfe92750796

Qwen/Qwen2.5-7B-Instruct
revision a09a35458c702b33eeacc393d103063234e8bc28
```

The archived generation metadata resolved to those revisions, although the historical generation code did not pass the revision argument explicitly. A strict reproduction should.

## HumanEval+ protocol

```text
EvalPlus             0.3.1
HumanEval+ release   v0.1.10
tasks                164
Kmax                 8
nested k             1, 2, 4, 8
temperature          0.8
top_p                0.95
max_new_tokens       384
generation seed      400401
dtype                 bfloat16
quantization         none
```

The dataset MD5 recorded by EvalPlus was:

```text
fe585eb4df8c88d844eeb463ea4d0302
```

The canonical public-task JSON SHA256 recorded before evaluation was:

```text
88707ade34a269bd1e038ddd8cdf12bbb71de115491520f777cebc581f64905e
```

## Required stage separation

A reproduction should preserve this ordering:

1. load only public task identifiers/prompts/entry points for inference;
2. generate the complete immutable candidate bank;
3. replay representations;
4. run frozen selectors;
5. write and hash selected candidate indices and trajectory hashes;
6. preferably commit or externally timestamp those manifests;
7. only then execute HumanEval+ tests;
8. attach evaluator outcomes and run statistics.

Step 6 is stronger than the archived run and closes the temporal-proof limitation documented in `AUDIT.md`.

## Evaluator isolation

Use the official EvalPlus containerized execution path or an equivalently isolated sandbox for generated code. The archived experiment used the official local evaluator because container execution was not available to that account, but local execution is not the preferred reproduction path.

## Analysis

Install the compact analysis package:

```bash
python -m pip install -e '.[test]'
pytest
```

Given archived `candidate_outcomes.csv` and `selected_outcomes.csv` files, the corrected public audit can be run with:

```bash
python -m capability_research.public_audit \
  --candidate-outcomes candidate_outcomes.csv \
  --selected-outcomes selected_outcomes.csv \
  --n 8 \
  --k 1 2 4 8
```

The script distinguishes:

- ordered prefix recoverability E_k;
- unbiased pass@k computed from the total number of successes in all n samples;
- selector accuracy at a specified bank size.

## Reproduction boundaries

The final manuscript makes no claim that the raw historical development environment can be bit-for-bit reconstructed from this publication repository alone. The purpose of this artifact is to preserve the frozen definitions, audited aggregate results, corrected statistics, and claim-relevant analysis code while excluding development clutter and sensitive operational material.
