import numpy as np
from tests.utils.generators import gen_UN
from tests.utils.algebra_api import mul, project
from tests.utils.oracles import interval_width_mul

SEED = 4242
TRIALS = 1000

def test_inv07_lambda1_mult_tightness():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng); y = gen_UN(rng)
        n_u = project(mul(x, y, lam=1.0))
        # compare widths
        w_u = 2 * n_u[1]
        w_int = interval_width_mul(project(x), project(y))
        assert w_u >= w_int - 1e-12
        # optional tightness check (can be relaxed in CI config)
        assert w_u <= 1.01 * w_int + 1e-12
