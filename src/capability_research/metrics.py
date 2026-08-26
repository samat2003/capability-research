from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from scipy.stats import binomtest


def pass_at_k(n: int, c: int, k: int) -> float:
    """Unbiased Codex pass@k estimator for n samples containing c successes.

    Important: ``c`` is the number of successful samples in the complete
    n-sample bank. It must not be recomputed from an ordered k-prefix.
    """
    n = int(n)
    c = int(c)
    k = int(k)
    if n <= 0 or not 0 <= c <= n or not 1 <= k <= n:
        raise ValueError(f"invalid n/c/k: n={n}, c={c}, k={k}")
    if c == 0:
        return 0.0
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


def empirical_recoverability(successes: Sequence[int | bool], k: int) -> int:
    """Whether an ordered candidate prefix contains at least one success."""
    if not 1 <= int(k) <= len(successes):
        raise ValueError("k must index a non-empty prefix of the bank")
    return int(any(bool(x) for x in successes[: int(k)]))


def first_correct(successes: Sequence[int | bool]) -> int | None:
    """One-indexed first successful sample, or None when the bank has no success."""
    for j, value in enumerate(successes, start=1):
        if bool(value):
            return j
    return None


def mean_unbiased_pass_at_k(banks: Iterable[Sequence[int | bool]], k: int) -> float:
    """Mean unbiased pass@k across fixed-size banks."""
    banks = [tuple(int(bool(x)) for x in bank) for bank in banks]
    if not banks:
        raise ValueError("at least one bank is required")
    n = len(banks[0])
    if any(len(bank) != n for bank in banks):
        raise ValueError("all banks must have the same sample count")
    return float(np.mean([pass_at_k(n, sum(bank), k) for bank in banks]))


@dataclass(frozen=True)
class PairedBinaryResult:
    mean_delta: float
    ci95_low: float
    ci95_high: float
    a_only: int
    b_only: int
    mcnemar_p: float


def paired_binary_test(
    a: Sequence[int | bool],
    b: Sequence[int | bool],
    *,
    seed: int = 0,
    bootstrap_replicates: int = 20_000,
) -> PairedBinaryResult:
    """Paired task bootstrap plus exact two-sided McNemar/binomial test."""
    aa = np.asarray(a, dtype=int)
    bb = np.asarray(b, dtype=int)
    if aa.ndim != 1 or bb.ndim != 1 or len(aa) != len(bb) or len(aa) == 0:
        raise ValueError("a and b must be non-empty paired one-dimensional arrays")
    if not np.isin(aa, [0, 1]).all() or not np.isin(bb, [0, 1]).all():
        raise ValueError("paired outcomes must be binary")

    delta = aa.astype(float) - bb.astype(float)
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(delta), size=(int(bootstrap_replicates), len(delta)))
    boot = delta[indices].mean(axis=1)

    a_only = int(((aa == 1) & (bb == 0)).sum())
    b_only = int(((aa == 0) & (bb == 1)).sum())
    discordant = a_only + b_only
    p = float(binomtest(a_only, discordant, 0.5).pvalue) if discordant else 1.0

    return PairedBinaryResult(
        mean_delta=float(delta.mean()),
        ci95_low=float(np.quantile(boot, 0.025)),
        ci95_high=float(np.quantile(boot, 0.975)),
        a_only=a_only,
        b_only=b_only,
        mcnemar_p=p,
    )
