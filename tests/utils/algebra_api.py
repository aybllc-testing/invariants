"""
Adapter layer: map tests to your library's API.
Replace stubs below with imports from your implementation.
"""
from typing import Tuple

UN = Tuple[Tuple[float, float], Tuple[float, float]]  # ((n_a,u_t),(n_m,u_m))

def add(x: UN, y: UN) -> UN:
    # Placeholder reference addition (component-wise conservative add)
    (na1, ut1), (nm1, um1) = x
    (na2, ut2), (nm2, um2) = y
    return ((na1 + na2, ut1 + ut2), (nm1 + nm2, um1 + um2))

def mul(x: UN, y: UN, lam: float = 1.0) -> UN:
    # U/N Multiplication (Definition 4) — interval-exact with λ parameter.
    # Source: un_algebra/core.py UNAlgebra.multiply()
    (na1, ut1), (nm1, um1) = x
    (na2, ut2), (nm2, um2) = y

    # Nominals: each tier multiplies independently
    na = na1 * na2
    nm = nm1 * nm2

    # Actual tier: linear cross-terms + cross-tier guard + quadratic
    u_t_tier   = abs(na1) * ut2 + abs(na2) * ut1
    cross_guard = abs(nm1) * ut2 + abs(nm2) * ut1
    quad_u_t   = lam * ut1 * ut2
    quad_cross = lam * (ut1 * um2 + um1 * ut2)
    ut = u_t_tier + cross_guard + quad_u_t + quad_cross

    # Measured tier: linear cross-terms + quadratic (no cross-tier guard needed)
    u_m_tier = abs(nm1) * um2 + abs(nm2) * um1
    quad_u_m = lam * um1 * um2
    um = u_m_tier + quad_u_m

    return ((na, ut), (nm, um))

def flip(x: UN) -> UN:
    (na, ut), (nm, um) = x
    return ((nm, um), (na, ut))

def catch(x: UN) -> UN:
    (na, ut), (nm, um) = x
    # Collapse actual tier to zero; preserve M = |na| + ut + |nm| + um.
    # M_after = 0 + 0 + |nm| + um_new = M_before  ⟹  um_new = |na| + ut + um
    return ((0.0, 0.0), (nm, abs(na) + ut + um))

def project(x: UN, known_na: bool = False) -> Tuple[float, float]:
    (na, ut), (nm, um) = x
    if known_na:
        return (nm, abs(nm - na) + um)
    return (nm, ut + um)
