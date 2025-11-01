import numpy as np
from tests.utils.generators import gen_UN, M
from tests.utils.algebra_api import flip
from tests.utils.ssot_loader import get_trials, get_seed

SEED = get_seed('properties')
TRIALS = get_trials(override=1000)

def test_inv06_flip_involution():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng)
        assert flip(flip(x)) == x
        assert M(flip(x)) == M(x)
