import numpy as np
import pytest
from tests.utils.generators import gen_UN, M
from tests.utils.algebra_api import add, mul, flip, catch, project
from tests.utils.ssot_loader import get_trials, get_seed, get_atol, get_rtol

SEED = get_seed('properties')
TRIALS = get_trials(override=2000)  # Use 2000 for local, can be overridden via SSOT_TRIALS env var
ATOL = get_atol()
RTOL = get_rtol()


def _tol(a, b):
    """Mixed absolute+relative tolerance for values at arbitrary scale."""
    return ATOL + RTOL * max(abs(a), abs(b))


def test_inv02_M_definition():
    """Test that M = |n_a| + u_t + |n_m| + u_m"""
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        un = gen_UN(rng)
        (n_a, u_t), (n_m, u_m) = un
        expected_M = abs(n_a) + u_t + abs(n_m) + u_m
        m = M(un)
        assert abs(m - expected_M) < _tol(m, expected_M), f"M definition mismatch: {m} vs {expected_M}"


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

        if delta > _tol(m_before, m_after):
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
        assert abs(m_after - m_before) < _tol(m_before, m_after), f"M not preserved under flip: {m_before} -> {m_after}"


def test_inv02_M_under_addition():
    """Test M behavior under addition - M should be sub-additive (conservative).
    M(x ⊕ y) ≤ M(x) + M(y) by triangle inequality on nominals:
    |na1+na2| ≤ |na1|+|na2| and |nm1+nm2| ≤ |nm1|+|nm2|.
    Exact equality does NOT hold in general.
    """
    rng = np.random.default_rng(SEED)
    violations = 0
    for _ in range(TRIALS):
        x = gen_UN(rng)
        y = gen_UN(rng)
        m_sum = M(add(x, y))
        m_bound = M(x) + M(y)
        # Sub-additivity: M(x ⊕ y) ≤ M(x) + M(y)
        # Allow rtol-scaled tolerance for floating-point equality at the boundary
        if m_sum > m_bound + ATOL + RTOL * max(abs(m_sum), abs(m_bound)):
            violations += 1
    assert violations == 0, f"M sub-additivity violated {violations}/{TRIALS} times"
