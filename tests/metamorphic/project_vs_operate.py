import numpy as np
from tests.utils.generators import gen_UN
from tests.utils.algebra_api import add, mul, project
from tests.utils.oracles import classical_add, classical_mul

SEED = 9001
TRIALS = 1000

def test_project_vs_operate():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng); y = gen_UN(rng)
        # add
        u_add = project(add(x,y))[1]
        c_add = classical_add(project(x), project(y))[1]
        assert u_add >= c_add
        # mul
        u_mul = project(mul(x,y,lam=1.0))[1]
        c_mul = classical_mul(project(x), project(y))[1]
        assert u_mul >= c_mul
