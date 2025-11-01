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
    # Simplified placeholder; replace with your λ-formula
    (na1, ut1), (nm1, um1) = x
    (na2, ut2), (nm2, um2) = y
    # Nominals multiply (measured and actual separately for placeholder)
    na = na1 * na2
    nm = nm1 * nm2
    # Uncertainty: linear terms + optional quadratic per λ
    u_lin = abs(na1) * ut2 + abs(na2) * ut1 + abs(nm1) * um2 + abs(nm2) * um1
    u_quad = lam * (ut1 * ut2 + um1 * um2)
    # Very conservative merge into both tiers (placeholder)
    return ((na, ut1 + ut2 + u_quad), (nm, um1 + um2 + u_lin))

def flip(x: UN) -> UN:
    (na, ut), (nm, um) = x
    return ((nm, um), (na, ut))

def catch(x: UN) -> UN:
    (na, ut), (nm, um) = x
    # Collapse actual tier to zero; absorb all uncertainty into measurement tier
    return ((0.0, 0.0), (nm, abs(nm - na) + ut + um))

def project(x: UN, known_na: bool = False) -> Tuple[float, float]:
    (na, ut), (nm, um) = x
    if known_na:
        return (nm, abs(nm - na) + um)
    return (nm, ut + um)
