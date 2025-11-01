# Reproducible & Cryptographically-Verifiable Runbook

This project is **self-running** and **cryptographically attestable**.

## One-command local verification
```bash
make verify
# or
scripts/run_self_verify.sh
```
This will:
1. Install pinned dependencies (`requirements.txt`).
2. Run the full test suite.
3. Produce a deterministic SHA-256 tree hash of the repo: `reporting/REPO_TREE_SHA256.txt`.

The file lists the sha256 of every tracked file (sorted) and ends with:
```
TREE_SHA256  <hex>
```

## Containerized (reproducible) run
```bash
make docker
```
Builds and runs tests in a minimal `python:3.11-slim` container.

## SBOM (software bill of materials)
Install `syft`, then:
```bash
make sbom
```
Creates `reporting/SBOM.spdx.json` for supply-chain transparency.

## Provenance & signing (bring-your-own keys)
Recommended:
- **Git commit signing:** GPG or SSH signatures.
- **Release signing:** `cosign sign-blob` the `reporting/REPO_TREE_SHA256.txt` and SBOM.
- **Container signing:** `cosign sign --key <key> un-algebra-tests:latest`
- **Provenance (SLSA):** Use GitHub OIDC + `cosign attest --predicate <provenance.json>`

### Example (sign the tree hash)
```bash
# Write the digest to a file (already done by scripts/hash_tree.py)
cat reporting/REPO_TREE_SHA256.txt

# Sign using cosign keypair (or keyless via OIDC)
cosign sign-blob --key cosign.key --output-signature reporting/REPO_TREE_SHA256.sig reporting/REPO_TREE_SHA256.txt

# Verify
cosign verify-blob --key cosign.pub --signature reporting/REPO_TREE_SHA256.sig reporting/REPO_TREE_SHA256.txt
```

## CI pipeline (GitHub Actions)
- Runs tests on every push/PR.
- You can extend `.github/workflows/tests.yml` to build the Docker image, generate an SBOM, and publish signed artifacts on release.

## Determinism notes
- Seeds are pinned in `tests/SSOT.yaml`.
- Dependencies are pinned in `requirements.txt`.
- The tree hash excludes transient artifacts (see `scripts/hash_tree.py`).

## Threat model (high level)
- **Integrity:** any change alters the TREE_SHA256; signatures/attestations bind a specific state.
- **Reproducibility:** container and pinned deps fix the execution environment.
- **Provenance:** CI can emit attestations linking commit → build → artifacts.


---

## CI Provenance (Keyless by default)
On tag pushes (e.g., `v1.0.0`), GitHub Actions:
1. Runs tests, computes TREE_SHA256, builds SBOM.
2. **Keylessly signs** `REPO_TREE_SHA256.txt` using OIDC (Fulcio).
3. **Attests** provenance with `cosign attest`.

Artifacts:
- `reports/` and `signed-reports/` in the workflow summary.

To verify keylessly, use:
```bash
COSIGN_EXPERIMENTAL=1 cosign verify-blob   --certificate-oidc-issuer https://token.actions.githubusercontent.com   --certificate-identity "https://github.com/OWNER/REPO/.github/workflows/provenance-and-signing.yml@refs/tags/v1.0.0"   --signature reporting/REPO_TREE_SHA256.sig   reporting/REPO_TREE_SHA256.txt
```
