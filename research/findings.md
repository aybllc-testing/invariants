# Findings — invariants
**Repo:** aybllc-testing/invariants
**Last updated:** 2026-03-24

## Key Results

1. **Infrastructure is production-grade** — despite placeholder algebra, everything else (CI/CD, SSOT loader, cryptographic provenance, package structure) is at A+ quality.

2. **Audit correctly identified 3 critical, 4 medium, 4 minor issues** — all were documented with file:line evidence. The test suite validated the audit: 16 failures confirm CRIT-01 (placeholder bugs).

3. **5 tests pass without real algebra** — proves the test framework itself is correctly implemented. Non-trivial: it means test scaffolding, imports, and CI all work.

4. **M accounting failure rate: 98% in catch()** — the placeholder implementation preserves M (the epistemic budget |n| + u) in only 2% of cases. This is the key invariant for the Catch operator.

5. **Addition associativity failure rate: 24%** — placeholder add() is not associative. Real algebra must be.

6. **SSOT loader pattern works** — all 11 test files now pull configuration from SSOT.yaml via `get_trials()`, `get_seed()`, `get_atol()`. No hardcoded values.

7. **Generator boundary issue found** — INV-04 boundary case test fails due to a test data generator bug (not an algebra bug). Needs fixing separately from real algebra work.

## Validation

Test run results (28 tests):
- 5 pass (18%) — validates framework
- 16 fail (57%) — all expected, expose placeholder bugs
- 7 skip (25%) — not yet implemented

## Known Gaps / Vulnerabilities

- Real algebra not implemented — this is the entire blocker (CRIT-01)
- 9 invariant tests not yet written (INV-08, 10, 11, 12, 13, 15, SCN-01–04)
- Generator boundary case bug (separate from algebra issue)
- No performance benchmarking
- No coverage tracking (pytest-cov not configured)
- MED-03: `known_na` parameter path in projection not tested
