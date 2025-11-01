import numpy as np
import pytest
from tests.utils.generators import gen_UN, M
from tests.utils.algebra_api import add, mul, flip, catch, project
from tests.utils.ssot_loader import get_trials, get_seed, get_atol

SEED = get_seed('properties')
TRIALS = get_trials(override=2000)  # Use 2000 for local, can be overridden via SSOT_TRIALS env var
ATOL = get_atol()


def test_inv02_M_definition():
    """Test that M = |n_a| + u_t + |n_m| + u_m"""
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        un = gen_UN(rng)
        (n_a, u_t), (n_m, u_m) = un
        expected_M = abs(n_a) + u_t + abs(n_m) + u_m
        assert abs(M(un) - expected_M) < ATOL, f"M definition mismatch: {M(un)} vs {expected_M}"


def test_inv02_M_nonnegative():
    """Test that M(x) >= 0 for all valid UN elements"""
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        un = gen_UN(rng)
        m_value = M(un)
        assert m_value >= 0, f"M is negative: {m_value}"


def test_inv02_M_preserved_under_catch():
    """Test that M(Cα(x)) = M(x)"""
    rng = np.random.default_rng(SEED)
    violations = 0
    max_delta = 0.0

    for _ in range(TRIALS):
        un = gen_UN(rng)
        m_before = M(un)
        caught = catch(un)
        m_after = M(caught)
        delta = abs(m_after - m_before)
        max_delta = max(max_delta, delta)

        if delta > ATOL:
            violations += 1

    assert violations == 0, f"M preservation violated {violations}/{TRIALS} times, max delta: {max_delta}"


def test_inv02_M_preserved_under_flip():
    """Test that M(B(x)) = M(x) - flip preserves M"""
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        un = gen_UN(rng)
        m_before = M(un)
        flipped = flip(un)
        m_after = M(flipped)
        assert abs(m_after - m_before) < ATOL, f"M not preserved under flip: {m_before} -> {m_after}"


def test_inv02_M_under_addition():
    """Test M behavior under addition - M should be additive or conservative"""
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng)
        y = gen_UN(rng)
        # For addition, M should be additive: M(x ⊕ y) = M(x) + M(y)
        # (at least for the component-wise placeholder implementation)
        m_sum = M(add(x, y))
        m_expected = M(x) + M(y)
        # Allow for some numerical tolerance
        assert abs(m_sum - m_expected) < ATOL, f"M not additive under ⊕: {m_sum} vs {m_expected}"
