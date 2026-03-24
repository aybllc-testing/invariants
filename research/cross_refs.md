# Cross-Repo References — invariants
**Repo:** aybllc-testing/invariants
**Last updated:** 2026-03-24

## Depends On

- **nu-algebra (N/U Algebra)** — the invariants (M accounting, associativity, sub-distributivity) are claimed properties of N/U Algebra. This test suite certifies them.
- **un-algebra (U/N Algebra)** — λ-parameterized multiplication is explicitly tested here (INV-09 tests associativity under λ).
- **unalgebra (UN Algebra)** — the PROGRESS.md says this is "UN algebra test suite" — refers to Uncertain Numbers algebra in the UN/N/U family.

## Used By

- Nothing depends on invariants as a library — it is a test runner.
- **Conceptually:** All algebra repos depend on this for certification. Once real algebra is implemented here and all 21 tests pass, that is the formal certification of correctness.

## Shared Artifacts

- **AUDIT_SSOT.yaml** — 1,380-line comprehensive audit document
- **FIXES.md** — 1,383-line implementation documentation
- **PROGRESS.md** — sprint progress report
- Repo: https://github.com/aybllc-testing/invariants
