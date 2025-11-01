import numpy as np
import pytest
from tests.utils.generators import gen_UN
from tests.utils.algebra_api import add, mul
from tests.utils.ssot_loader import get_trials, get_seed, get_atol

SEED = get_seed('properties')
TRIALS = get_trials(override=2000)
ATOL = get_atol()


def test_inv14_subdistributivity_nominals_equal():
    """
    Test that nominals are equal for x ⊗ (y ⊕ z) and (x ⊗ y) ⊕ (x ⊗ z).
    Standard distributivity holds for nominals.
    """
    rng = np.random.default_rng(SEED)
    violations = 0

    for _ in range(TRIALS):
        x = gen_UN(rng)
        y = gen_UN(rng)
        z = gen_UN(rng)

        # Left: x ⊗ (y ⊕ z)
        left = mul(x, add(y, z), lam=1.0)
        (na_l, ut_l), (nm_l, um_l) = left

        # Right: (x ⊗ y) ⊕ (x ⊗ z)
        right = add(mul(x, y, lam=1.0), mul(x, z, lam=1.0))
        (na_r, ut_r), (nm_r, um_r) = right

        # Check nominal equality
        if abs(na_l - na_r) > ATOL or abs(nm_l - nm_r) > ATOL:
            violations += 1

    assert violations == 0, f"Nominal distributivity violated {violations}/{TRIALS} times"


def test_inv14_subdistributivity_uncertainties():
    """
    Test that uncertainties satisfy x ⊗ (y ⊕ z) ⪯ (x ⊗ y) ⊕ (x ⊗ z).
    The left side (direct) should have tighter or equal uncertainties than the right (distributed).
    """
    rng = np.random.default_rng(SEED)
    violations_ut = 0
    violations_um = 0
    max_excess_ut = 0.0
    max_excess_um = 0.0

    for _ in range(TRIALS):
        x = gen_UN(rng)
        y = gen_UN(rng)
        z = gen_UN(rng)

        # Left: x ⊗ (y ⊕ z)
        left = mul(x, add(y, z), lam=1.0)
        (na_l, ut_l), (nm_l, um_l) = left

        # Right: (x ⊗ y) ⊕ (x ⊗ z)
        right = add(mul(x, y, lam=1.0), mul(x, z, lam=1.0))
        (na_r, ut_r), (nm_r, um_r) = right

        # Check sub-distributivity: left uncertainties <= right uncertainties
        excess_ut = ut_l - ut_r
        excess_um = um_l - um_r

        if excess_ut > ATOL:
            violations_ut += 1
            max_excess_ut = max(max_excess_ut, excess_ut)

        if excess_um > ATOL:
            violations_um += 1
            max_excess_um = max(max_excess_um, excess_um)

    assert violations_ut == 0, (
        f"Sub-distributivity violated for u_t: {violations_ut}/{TRIALS} times, "
        f"max excess: {max_excess_ut}"
    )
    assert violations_um == 0, (
        f"Sub-distributivity violated for u_m: {violations_um}/{TRIALS} times, "
        f"max excess: {max_excess_um}"
    )


def test_inv14_subdistributivity_combined():
    """
    Test combined sub-distributivity: both tiers should satisfy the constraint.
    """
    rng = np.random.default_rng(SEED)
    violations = 0

    for _ in range(TRIALS):
        x = gen_UN(rng)
        y = gen_UN(rng)
        z = gen_UN(rng)

        # Left: x ⊗ (y ⊕ z)
        left = mul(x, add(y, z), lam=1.0)

        # Right: (x ⊗ y) ⊕ (x ⊗ z)
        right = add(mul(x, y, lam=1.0), mul(x, z, lam=1.0))

        # Check that left ⪯ right (componentwise)
        (na_l, ut_l), (nm_l, um_l) = left
        (na_r, ut_r), (nm_r, um_r) = right

        # Nominals should be equal (tested above)
        # Uncertainties should satisfy ut_l <= ut_r and um_l <= um_r
        if ut_l > ut_r + ATOL or um_l > um_r + ATOL:
            violations += 1

    assert violations == 0, f"Combined sub-distributivity violated {violations}/{TRIALS} times"
