import numpy as np
from tests.utils.generators import gen_UN
from tests.utils.algebra_api import add, mul, project
from tests.utils.oracles import classical_add, classical_mul
from tests.utils.ssot_loader import get_trials, get_seed

SEED = get_seed('properties')
TRIALS = get_trials(override=2000)

def test_inv03_projection_conservativity_add():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng); y = gen_UN(rng)
        n_u = project(add(x, y))
        n_c = classical_add(project(x), project(y))
        assert n_u[1] >= n_c[1]

def test_inv03_projection_conservativity_mul():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng); y = gen_UN(rng)
        n_u = project(mul(x, y, lam=1.0))
        n_c = classical_mul(project(x), project(y))
        assert n_u[1] >= n_c[1]
