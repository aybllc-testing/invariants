.PHONY: test build docker sbom hash verify clean

PYTHON ?= python3

test:
	$(PYTHON) -m pytest -q tests

hash:
	$(PYTHON) scripts/hash_tree.py --out reporting/REPO_TREE_SHA256.txt

verify: test hash

build:
	$(PYTHON) -m pip install -r requirements.txt

docker:
	docker build -t un-algebra-tests:latest .
	docker run --rm -e CI=1 un-algebra-tests:latest

sbom:
	@which syft >/dev/null 2>&1 || (echo "Install syft: https://github.com/anchore/syft" && exit 1)
	syft packages dir:. -o spdx-json=reporting/SBOM.spdx.json

clean:
	rm -f reporting/REPO_TREE_SHA256.txt reporting/SBOM.spdx.json

sign-local:
	@which cosign >/dev/null 2>&1 || (echo "Install cosign: https://docs.sigstore.dev/cosign/overview/" && exit 1)
	cosign sign-blob --yes --key cosign.key --output-signature reporting/REPO_TREE_SHA256.sig reporting/REPO_TREE_SHA256.txt

verify-local:
	@which cosign >/dev/null 2>&1 || (echo "Install cosign" && exit 1)
	cosign verify-blob --key cosign.pub --signature reporting/REPO_TREE_SHA256.sig reporting/REPO_TREE_SHA256.txt
