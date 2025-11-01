import numpy as np
from tests.utils.generators import gen_UN
from tests.utils.algebra_api import mul, project
from tests.utils.oracles import interval_width_mul
from tests.utils.ssot_loader import get_trials, get_seed, get_threshold, get_atol

SEED = get_seed('properties')
TRIALS = get_trials(override=1000)
ATOL = get_atol()
TIGHTNESS_THRESHOLD = get_threshold('tightness_r_p99_9')  # 1.001 from SSOT

def test_inv07_lambda1_mult_tightness():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng); y = gen_UN(rng)
        n_u = project(mul(x, y, lam=1.0))
        # compare widths
        w_u = 2 * n_u[1]
        w_int = interval_width_mul(project(x), project(y))
        assert w_u >= w_int - ATOL
        # optional tightness check (can be relaxed in CI config)
        assert w_u <= TIGHTNESS_THRESHOLD * w_int + ATOL
