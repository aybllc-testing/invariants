import numpy as np
from tests.utils.generators import gen_UN, M
from tests.utils.algebra_api import flip
from tests.utils.ssot_loader import get_trials, get_seed, get_atol, get_rtol

SEED = get_seed('properties')
TRIALS = get_trials(override=1000)
ATOL = get_atol()
RTOL = get_rtol()


def _m_close(a, b):
    return abs(a - b) < ATOL + RTOL * max(abs(a), abs(b))


def _un_close(x, y):
    """Component-wise mixed-tolerance equality for UN pairs."""
    (na1, ut1), (nm1, um1) = x
    (na2, ut2), (nm2, um2) = y
    return (
        abs(na1 - na2) < ATOL + RTOL * max(abs(na1), abs(na2)) and
        abs(ut1 - ut2) < ATOL + RTOL * max(abs(ut1), abs(ut2)) and
        abs(nm1 - nm2) < ATOL + RTOL * max(abs(nm1), abs(nm2)) and
        abs(um1 - um2) < ATOL + RTOL * max(abs(um1), abs(um2))
    )


def test_inv06_flip_involution():
    rng = np.random.default_rng(SEED)
    for _ in range(TRIALS):
        x = gen_UN(rng)
        assert _un_close(flip(flip(x)), x), f"flip(flip(x)) != x: {flip(flip(x))} vs {x}"
        assert _m_close(M(flip(x)), M(x)), f"M not preserved under flip: {M(flip(x))} vs {M(x)}"
