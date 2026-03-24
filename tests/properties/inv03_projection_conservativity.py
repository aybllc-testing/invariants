import numpy as np
from tests.utils.generators import gen_UN
from tests.utils.algebra_api import add, mul, project
from tests.utils.oracles import classical_add, classical_mul
from tests.utils.ssot_loader import get_trials, get_seed, get_atol, get_rtol

SEED = get_seed('properties')
TRIALS = get_trials(override=2000)
ATOL = get_atol()
RTOL = get_rtol()

def test_inv03_projection_conservativity_add():
    # project(add(x,y)).u = (ut1+ut2)+(um1+um2)
    # classical_add(project(x),project(y)).u = (ut1+um1)+(ut2+um2)
    # These are mathematically equal; floating-point addition order can differ at high scale.
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng); y = gen_UN(rng)
        n_u = project(add(x, y))
        n_c = classical_add(project(x), project(y))
        tol = ATOL + RTOL * max(abs(n_u[1]), abs(n_c[1]))
        assert n_u[1] >= n_c[1] - tol, f"Projection conservativity add: {n_u[1]} < {n_c[1]} - {tol}"

def test_inv03_projection_conservativity_mul():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng); y = gen_UN(rng)
        n_u = project(mul(x, y, lam=1.0))
        n_c = classical_mul(project(x), project(y))
        assert n_u[1] >= n_c[1]
