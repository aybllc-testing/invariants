import numpy as np
from tests.utils.generators import gen_UN, M
from tests.utils.algebra_api import mul
from tests.utils.ssot_loader import get_trials, get_seed, get_atol

SEED = get_seed('properties')
TRIALS = get_trials(override=2000)
ATOL = get_atol()

def test_inv05_M_monotonicity_mult():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng); y = gen_UN(rng)
        lhs = M(mul(x, y, lam=1.0))
        rhs = M(x) * M(y)
        assert lhs <= rhs + ATOL
