"""
SSOT Configuration Loader
Loads test configuration from tests/SSOT.yaml
"""
import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional

_SSOT_CACHE: Optional[Dict[str, Any]] = None


def get_ssot_path() -> Path:
    """Get the path to SSOT.yaml file."""
    # Assume we're in tests/utils/ and SSOT is in tests/
    return Path(__file__).parent.parent / "SSOT.yaml"


def load_ssot() -> Dict[str, Any]:
    """Load SSOT configuration from YAML file."""
    global _SSOT_CACHE
    if _SSOT_CACHE is not None:
        return _SSOT_CACHE

    ssot_path = get_ssot_path()
    if not ssot_path.exists():
        raise FileNotFoundError(f"SSOT file not found: {ssot_path}")

    with open(ssot_path, 'r') as f:
        _SSOT_CACHE = yaml.safe_load(f)

    return _SSOT_CACHE


def get_trials(override: Optional[int] = None) -> int:
    """
    Get number of trials per test.

    Args:
        override: Optional override value (e.g., for smoke tests)

    Returns:
        Number of trials from SSOT or override
    """
    if override is not None:
        return override

    # Check for environment variable override (for CI)
    env_trials = os.environ.get('SSOT_TRIALS')
    if env_trials:
        return int(env_trials)

    ssot = load_ssot()
    return ssot.get('defaults', {}).get('trials_per_test', 50000)


def get_seed(category: str = 'properties') -> int:
    """
    Get seed for a specific test category.

    Args:
        category: One of 'global', 'properties', 'metamorphic', 'scenarios'

    Returns:
        Seed value from SSOT
    """
    ssot = load_ssot()
    seeds = ssot.get('defaults', {}).get('seeds', {})
    return seeds.get(category, seeds.get('global', 1337))


def get_tolerance(kind: str = 'atol') -> float:
    """
    Get tolerance value from SSOT.

    Args:
        kind: Either 'atol' (absolute) or 'rtol' (relative)

    Returns:
        Tolerance value
    """
    ssot = load_ssot()
    value = ssot.get('defaults', {}).get(kind, 1e-12)
    # Handle both string and numeric representations
    if isinstance(value, str):
        return float(value)
    return float(value) if value is not None else 1e-12


def get_threshold(name: str) -> float:
    """
    Get threshold value from SSOT.

    Args:
        name: Threshold name (e.g., 'tightness_r_p99_9', 'M_ratio_max')

    Returns:
        Threshold value
    """
    ssot = load_ssot()
    thresholds = ssot.get('defaults', {}).get('thresholds', {})

    # Handle special string values like "3/N"
    value = thresholds.get(name)
    if isinstance(value, str):
        # For now, return as string - caller must handle
        return value

    return float(value) if value is not None else None


def get_invariant_spec(inv_id: str) -> Optional[Dict[str, Any]]:
    """
    Get specification for a specific invariant.

    Args:
        inv_id: Invariant ID (e.g., 'INV-01', 'INV-02')

    Returns:
        Invariant specification dict or None
    """
    ssot = load_ssot()
    invariants = ssot.get('invariants', [])

    for inv in invariants:
        if inv.get('id') == inv_id:
            return inv

    return None


# Convenience constants
ATOL = None  # Lazy loaded
RTOL = None  # Lazy loaded


def get_atol() -> float:
    """Get absolute tolerance (cached)."""
    global ATOL
    if ATOL is None:
        ATOL = get_tolerance('atol')
    return ATOL


def get_rtol() -> float:
    """Get relative tolerance (cached)."""
    global RTOL
    if RTOL is None:
        RTOL = get_tolerance('rtol')
    return RTOL
