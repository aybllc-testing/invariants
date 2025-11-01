import numpy as np
import pytest
from tests.utils.generators import gen_UN, boundary_ok
from tests.utils.algebra_api import add, mul, flip, catch

SEED = 4242
TRIALS = 2000  # keep smoke tests light; raise in CI if desired

def check_all_ops(un):
    assert boundary_ok(un, atol=1e-15)
    # add with another sample
    rng = np.random.default_rng(SEED)
    other = gen_UN(rng)
    assert boundary_ok(add(un, other), atol=1e-15)
    # mul with another sample
    assert boundary_ok(mul(un, other, lam=1.0), atol=1e-15)
    # flip
    assert boundary_ok(flip(un), atol=1e-15)
    # catch
    assert boundary_ok(catch(un), atol=1e-15)

def test_inv01_triangle_smoke():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        un = gen_UN(rng)
        check_all_ops(un)
