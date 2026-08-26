from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import pandas as pd

from .metrics import empirical_recoverability, mean_unbiased_pass_at_k


def load_candidate_banks(path: str | Path, n: int) -> dict[str, list[int]]:
    """Load and validate ordered binary candidate outcomes.

    Expected columns: task_id, sample_index, success.
    """
    df = pd.read_csv(path)
    required = {"task_id", "sample_index", "success"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"missing candidate columns: {sorted(missing)}")

    banks: dict[str, list[int]] = {}
    for task_id, group in df.groupby("task_id", sort=True):
        group = group.sort_values("sample_index")
        indices = group["sample_index"].astype(int).tolist()
        if indices != list(range(n)):
            raise ValueError(f"{task_id}: expected sample indices 0..{n-1}, got {indices}")
        values = group["success"].astype(int).tolist()
        if not set(values).issubset({0, 1}):
            raise ValueError(f"{task_id}: non-binary success values")
        banks[str(task_id)] = values

    if not banks:
        raise ValueError("no candidate outcomes found")
    return banks


def load_selected(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"task_id", "k", "arm", "sample_index", "success"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"missing selection columns: {sorted(missing)}")
    return df


def audit(candidate_path: str | Path, selected_path: str | Path, n: int, ks: list[int]) -> dict:
    banks = load_candidate_banks(candidate_path, n)
    selected = load_selected(selected_path)

    recoverability = {}
    for k in ks:
        if not 1 <= k <= n:
            raise ValueError(f"invalid k={k} for n={n}")
        e = [empirical_recoverability(bank, k) for bank in banks.values()]
        recoverability[str(k)] = {
            "ordered_E_k": sum(e) / len(e),
            "ordered_E_successes": int(sum(e)),
            # Correct estimator: c comes from every sample in the complete n-sample bank.
            "unbiased_pass_at_k": mean_unbiased_pass_at_k(banks.values(), k),
        }

    arms = defaultdict(dict)
    for row in selected.itertuples(index=False):
        key = (str(row.arm), int(row.k))
        task_id = str(row.task_id)
        if task_id in arms[key]:
            raise ValueError(f"duplicate selected outcome for {key} / {task_id}")
        arms[key][task_id] = int(row.success)

    selection_summary = {}
    task_ids = set(banks)
    for (arm, k), by_task in sorted(arms.items()):
        if set(by_task) != task_ids:
            raise ValueError(f"{arm}@{k}: selection task set differs from candidate task set")
        values = list(by_task.values())
        selection_summary[f"{arm}@{k}"] = {
            "successes": int(sum(values)),
            "tasks": len(values),
            "accuracy": sum(values) / len(values),
        }

    return {
        "tasks": len(banks),
        "samples_per_task": n,
        "recoverability": recoverability,
        "selection": selection_summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit ordered recoverability and corrected pass@k")
    parser.add_argument("--candidate-outcomes", required=True)
    parser.add_argument("--selected-outcomes", required=True)
    parser.add_argument("--n", required=True, type=int)
    parser.add_argument("--k", nargs="+", required=True, type=int)
    parser.add_argument("--out")
    args = parser.parse_args()

    result = audit(args.candidate_outcomes, args.selected_outcomes, args.n, args.k)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
