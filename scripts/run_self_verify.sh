#!/usr/bin/env bash
set -euo pipefail

echo "[1/3] Installing deps..."
python3 -m pip install -r requirements.txt

echo "[2/3] Running tests..."
pytest -q tests

echo "[3/3] Computing repo tree hash..."
python3 scripts/hash_tree.py --out reporting/REPO_TREE_SHA256.txt

echo "Repo tree hash saved to reporting/REPO_TREE_SHA256.txt"
