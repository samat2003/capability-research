import math

from capability_research.metrics import (
    empirical_recoverability,
    mean_unbiased_pass_at_k,
    pass_at_k,
)


def test_pass_at_k_uses_full_bank_success_count():
    bank = [0, 0, 0, 0, 0, 0, 1, 0]
    assert empirical_recoverability(bank, 1) == 0
    assert empirical_recoverability(bank, 4) == 0
    assert empirical_recoverability(bank, 8) == 1

    # Unbiased pass@1 for an eight-sample bank with one success is 1/8,
    # even though the success is not in the ordered first-one prefix.
    assert math.isclose(pass_at_k(8, sum(bank), 1), 1 / 8)


def test_mean_pass_at_k_does_not_truncate_before_counting_c():
    banks = [
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert math.isclose(mean_unbiased_pass_at_k(banks, 1), 1 / 16)


def test_pass_at_n_equals_pool_recoverability_per_task():
    for c in range(9):
        expected = 0.0 if c == 0 else 1.0
        assert pass_at_k(8, c, 8) == expected
