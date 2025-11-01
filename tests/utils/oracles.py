from typing import Tuple
import math

NU = Tuple[float, float]  # (n, u)

def classical_add(x: NU, y: NU) -> NU:
    nx, ux = x; ny, uy = y
    return (nx + ny, ux + uy)

def classical_mul(x: NU, y: NU) -> NU:
    nx, ux = x; ny, uy = y
    n = nx * ny
    u = abs(nx) * uy + abs(ny) * ux + ux * uy  # interval-exact for symmetric intervals
    return (n, u)

def interval_width_mul(x: NU, y: NU) -> float:
    nx, ux = x; ny, uy = y
    # compute [nx-ux, nx+ux] * [ny-uy, ny+uy] interval width
    a, b = nx - ux, nx + ux
    c, d = ny - uy, ny + uy
    products = [a*c, a*d, b*c, b*d]
    return max(products) - min(products)
