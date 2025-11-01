import numpy as np
from tests.utils.generators import gen_UN, M
from tests.utils.algebra_api import mul

SEED = 4242
TRIALS = 2000

def test_inv05_M_monotonicity_mult():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng); y = gen_UN(rng)
        lhs = M(mul(x, y, lam=1.0))
        rhs = M(x) * M(y)
        assert lhs <= rhs + 1e-12
