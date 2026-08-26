# Security note

This repository is a clean publication artifact. It intentionally excludes machine-access credentials, local workstation paths, authentication material, host-specific connection instructions, model caches, private runtime logs, and development-agent transcripts.

No generated program should be executed directly on a trusted workstation as part of benchmark reproduction. Use the official EvalPlus containerized evaluator or an equivalently isolated sandbox.

If sensitive operational material is ever discovered in this repository, remove it from the public artifact and rotate any affected credential outside the repository. Do not preserve secret-bearing development history for reproducibility; use sanitized provenance hashes and scientific artifacts instead.
