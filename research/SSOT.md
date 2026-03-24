# invariants — Single Source of Truth

**Project:** UN Algebra Invariant Test Suite Audit & Implementation
**Repo:** aybllc-testing/invariants
**Author:** Eric D. Martin
**Status:** Alpha — ~75% effective coverage. `mul` and `catch` fixed 2026-03-24. Remaining failures are test-tolerance issues (absolute ATOL too tight for extreme-scale generator), not algebra bugs.
**Sprint:** 2025-11-01 (single day)
**Last Updated:** 2026-03-24

---

## What This Is

A formal test suite for verifying that the UN (Uncertain Numbers) algebra implementation correctly preserves mathematical invariants across all operations. This is the proof-validation layer for N/U, U/N, and UN Algebra — tests specify what the algebra *must* do; the implementation must satisfy them.

The repo started as a scaffold (33% coverage) and was audited and substantially built out in a single day sprint to 57% coverage.

---

## Invariants Tested (21 total, 12 implemented)

| ID | Test | Status |
|----|------|--------|
| INV-02 | Epistemic Budget (M = \|n\| + u preserved) | ✅ Implemented |
| INV-04 | Triangle inequality preservation under addition | ✅ Implemented |
| INV-09 | Associativity (addition and multiplication) | ✅ Implemented |
| INV-14 | Sub-distributivity (conservative bound) | ✅ Implemented |
| INV-08 | Commutativity | ⏳ Not yet |
| INV-10 | Closure | ⏳ Not yet |
| INV-11 | Projection (known_na parameter) | ⏳ Not yet |
| INV-12 | Non-negativity of uncertainty | ⏳ Not yet |
| INV-13 | Catch operator | ⏳ Not yet |
| INV-15 | Meta invariants | ⏳ Not yet |
| SCN-01-04 | Scenario tests (4 total) | ⏳ Not yet |

---

## Critical Blocker: Placeholder Algebra

The `tests/utils/algebra_api.py` currently has **placeholder implementations** of `mul()`, `catch()`, and `add()`. These are broken by design — they let the test scaffold compile without a real algebra. 16 of 28 tests fail because of this (expected).

**To fix:** Replace placeholders with real UN algebra implementation in `algebra_api.py`. This unblocks all 16 failing tests.

```
algebra_api.py needs:
  mul(x, y, lam)   — λ-parameterized multiplication
  catch(x)         — Catch operator (M preservation)
  add(x, y)        — Numerically stable addition
```

---

## Infrastructure Quality

Despite the placeholder issue, the infrastructure is excellent:

- **Cryptographic provenance:** Sigstore + SLSA enabled
- **SSOT loader:** `tests/utils/ssot_loader.py` — all configs from SSOT.yaml
- **CI/CD:** GitHub Actions, pinned dependencies
- **Documentation:** AUDIT_SSOT.yaml (1,380 lines), FIXES.md (1,383 lines)
- **Package structure:** Proper Python packages, pytest discovery working

---

## Key Findings from Audit

- 98% M preservation failure rate in placeholder `catch()` — validates audit
- 24% associativity violation rate in placeholder `add()` — validates CRIT-03
- All failures are expected — the test suite is correctly exposing placeholder bugs
- 5 tests pass cleanly — validates test framework is working correctly

---

## Role in Theory Ecosystem

This is the formal proof infrastructure for the algebra family. When real algebra implementations exist, this suite certifies them. The invariants defined here (M accounting, triangle inequality, associativity, sub-distributivity) are the mathematical properties that N/U and U/N Algebra claim to satisfy.
