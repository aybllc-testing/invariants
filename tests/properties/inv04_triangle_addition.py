import numpy as np
import pytest
from tests.utils.generators import gen_UN, boundary_ok
from tests.utils.algebra_api import add
from tests.utils.ssot_loader import get_trials, get_seed, get_atol

SEED = get_seed('properties')
TRIALS = get_trials(override=2000)
ATOL = get_atol()


def test_inv04_triangle_preservation_addition():
    """
    Test that Triangle(x) ∧ Triangle(y) ⇒ Triangle(x ⊕ y).
    If both x and y satisfy the triangle inequality, their sum should too.
    """
    rng = np.random.default_rng(SEED)
    violations = 0

    for _ in range(TRIALS):
        x = gen_UN(rng)
        y = gen_UN(rng)

        # Verify inputs satisfy triangle inequality
        assert boundary_ok(x, atol=ATOL), "Generated x violates triangle inequality"
        assert boundary_ok(y, atol=ATOL), "Generated y violates triangle inequality"

        # Compute sum
        result = add(x, y)

        # Check that result satisfies triangle inequality
        if not boundary_ok(result, atol=ATOL):
            violations += 1

    assert violations == 0, f"Triangle preservation violated {violations}/{TRIALS} times"


def test_inv04_triangle_boundary_cases():
    """
    Test triangle preservation with boundary cases where triangle inequality is exact.
    """
    rng = np.random.default_rng(SEED)

    for _ in range(100):  # Smaller number for boundary cases
        # Create values at exact boundary: |n_m - n_a| = u_t + u_m
        s = 10 ** rng.uniform(-6, 6)
        n_a = rng.normal() * s
        u_t = abs(rng.normal()) * s
        u_m = abs(rng.normal()) * s

        # Set n_m to be exactly at boundary
        sign = 1 if rng.random() > 0.5 else -1
        n_m = n_a + sign * (u_t + u_m)

        x = ((n_a, u_t), (n_m, u_m))

        # Do the same for y
        n_a2 = rng.normal() * s
        u_t2 = abs(rng.normal()) * s
        u_m2 = abs(rng.normal()) * s
        sign2 = 1 if rng.random() > 0.5 else -1
        n_m2 = n_a2 + sign2 * (u_t2 + u_m2)

        y = ((n_a2, u_t2), (n_m2, u_m2))

        # Verify boundary condition
        assert abs(abs(n_m - n_a) - (u_t + u_m)) < 1e-10, "Boundary not exact"
        assert abs(abs(n_m2 - n_a2) - (u_t2 + u_m2)) < 1e-10, "Boundary not exact"

        # Add them
        result = add(x, y)

        # Result should still satisfy triangle (possibly at boundary)
        assert boundary_ok(result, atol=ATOL), "Triangle violated at boundary case"


def test_inv04_componentwise_addition():
    """
    Verify that component-wise addition preserves triangle inequality.
    For addition: (n_a1+n_a2, u_t1+u_t2), (n_m1+n_m2, u_m1+u_m2)
    """
    rng = np.random.default_rng(SEED)

    for _ in range(TRIALS):
        x = gen_UN(rng)
        y = gen_UN(rng)

        (na1, ut1), (nm1, um1) = x
        (na2, ut2), (nm2, um2) = y

        # Addition is component-wise
        result = add(x, y)
        (na_r, ut_r), (nm_r, um_r) = result

        # Verify component-wise addition
        assert abs(na_r - (na1 + na2)) < ATOL
        assert abs(ut_r - (ut1 + ut2)) < ATOL
        assert abs(nm_r - (nm1 + nm2)) < ATOL
        assert abs(um_r - (um1 + um2)) < ATOL

        # Now verify triangle inequality for result
        # |n_m - n_a| ≤ u_t + u_m becomes
        # |(nm1+nm2) - (na1+na2)| ≤ (ut1+ut2) + (um1+um2)
        # = |(nm1-na1) + (nm2-na2)| ≤ (ut1+um1) + (ut2+um2)
        # By triangle inequality of absolute values and the fact that
        # |nm1-na1| ≤ ut1+um1 and |nm2-na2| ≤ ut2+um2, this should hold

        assert boundary_ok(result, atol=ATOL)
