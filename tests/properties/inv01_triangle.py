import numpy as np
import pytest
from tests.utils.generators import gen_UN, boundary_ok
from tests.utils.algebra_api import add, mul, flip, catch
from tests.utils.ssot_loader import get_trials, get_seed, get_atol

SEED = get_seed('properties')
TRIALS = get_trials(override=2000)  # Use 2000 for local; can be overridden via SSOT_TRIALS env var
ATOL = get_atol()

def check_all_ops(un):
    assert boundary_ok(un, atol=ATOL)
    # add with another sample
    rng = np.random.default_rng(SEED)
    other = gen_UN(rng)
    assert boundary_ok(add(un, other), atol=ATOL)
    # mul with another sample
    assert boundary_ok(mul(un, other, lam=1.0), atol=ATOL)
    # flip
    assert boundary_ok(flip(un), atol=ATOL)
    # catch
    assert boundary_ok(catch(un), atol=ATOL)

def test_inv01_triangle_smoke():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        un = gen_UN(rng)
        check_all_ops(un)
