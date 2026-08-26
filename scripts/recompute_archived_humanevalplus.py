from __future__ import annotations

import argparse
import json
from pathlib import Path

from capability_research.metrics import (
    empirical_recoverability,
    mean_unbiased_pass_at_k,
)
from capability_research.public_audit import load_candidate_banks


def summarize(path: str | Path, n: int, ks: list[int]) -> dict:
    banks = load_candidate_banks(path, n)
    return {
        "tasks": len(banks),
        "samples_per_task": n,
        "total_successful_candidates": int(sum(sum(bank) for bank in banks.values())),
        "ordered_recoverability": {
            str(k): {
                "successes": int(sum(empirical_recoverability(bank, k) for bank in banks.values())),
                "accuracy": float(
                    sum(empirical_recoverability(bank, k) for bank in banks.values()) / len(banks)
                ),
            }
            for k in ks
        },
        "unbiased_pass_at_k": {
            str(k): mean_unbiased_pass_at_k(banks.values(), k) for k in ks
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--instruct", required=True)
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--k", type=int, nargs="+", default=[1, 2, 4, 8])
    parser.add_argument("--out")
    args = parser.parse_args()

    result = {
        "base": summarize(args.base, args.n, args.k),
        "instruct": summarize(args.instruct, args.n, args.k),
    }
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
