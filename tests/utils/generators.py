import numpy as np

def gen_UN(rng: np.random.Generator):
    """
    Generate a valid U/N element: ((n_a, u_t), (n_m, u_m))
    Ensures u_t,u_m >= 0 and |n_m - n_a| <= u_t + u_m (biased to boundary).
    """
    # magnitude scale
    s = 10 ** rng.uniform(-12, 12)
    n_a = rng.normal() * s
    # provisional n_m
    n_m = n_a + rng.normal() * s
    # nonnegative uncertainties
    u_t = abs(rng.normal()) * s
    u_m = abs(rng.normal()) * s

    d = abs(n_m - n_a)
    if d > u_t + u_m:
        # enforce triangle; push near boundary with tiny slack
        slack = s * 1e-12
        bump = d - (u_t + u_m) + slack
        share = rng.uniform(0.2, 0.8)
        u_t += bump * share
        u_m += bump * (1.0 - share)
    return ((n_a, max(u_t, 0.0)), (n_m, max(u_m, 0.0)))

def M(un):
    """Epistemic budget M = |n_a| + u_t + |n_m| + u_m"""
    (n_a, u_t), (n_m, u_m) = un
    return abs(n_a) + u_t + abs(n_m) + u_m

def boundary_ok(un, atol=0.0):
    """Check triangle inequality (with optional tolerance)."""
    (n_a, u_t), (n_m, u_m) = un
    return abs(n_m - n_a) <= u_t + u_m + atol
