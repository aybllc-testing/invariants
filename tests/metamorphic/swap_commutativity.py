import numpy as np
from tests.utils.generators import gen_UN
from tests.utils.algebra_api import add, mul

SEED = 9001
TRIALS = 1000

def test_commutativity_meta():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng); y = gen_UN(rng)
        assert add(x,y) == add(y,x)
        assert mul(x,y,lam=1.0) == mul(y,x,lam=1.0)
