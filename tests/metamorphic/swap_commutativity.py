import numpy as np
from tests.utils.generators import gen_UN
from tests.utils.algebra_api import add, mul
from tests.utils.ssot_loader import get_trials, get_seed

SEED = get_seed('metamorphic')
TRIALS = get_trials(override=1000)

def test_commutativity_meta():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng); y = gen_UN(rng)
        assert add(x,y) == add(y,x)
        assert mul(x,y,lam=1.0) == mul(y,x,lam=1.0)
