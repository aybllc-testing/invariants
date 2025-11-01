#!/usr/bin/env python3
import argparse, hashlib, os, sys

EXCLUDE_DIRS = {'.git', '__pycache__', '.venv', 'venv', '.mypy_cache', '.pytest_cache', '.github'}
EXCLUDE_FILES = {'REPO_TREE_SHA256.txt', 'SBOM.spdx.json', '.DS_Store'}

def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        # prune excluded dirs
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in sorted(filenames):
            if f in EXCLUDE_FILES:
                continue
            yield os.path.relpath(os.path.join(dirpath, f), root)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fp:
        for chunk in iter(lambda: fp.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='reporting/REPO_TREE_SHA256.txt')
    ap.add_argument('--root', default='.')
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    digests = []
    for rel in iter_files(root):
        full = os.path.join(root, rel)
        if not os.path.isfile(full):
            continue
        digests.append((rel.replace('\\','/'), sha256_file(full)))

    # deterministic tree hash: hash of the newline-joined "hash  path" lines
    lines = [f"{h}  {p}" for (p,h) in sorted((p,h) for (p,h) in digests)]
    tree = "\n".join(lines).encode('utf-8')
    tree_hash = hashlib.sha256(tree).hexdigest()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w') as fp:
        fp.write("# sha256 of each file (sorted) and repo-tree sha256 at bottom\n")
        fp.write("\n".join(lines))
        fp.write("\n\nTREE_SHA256  " + tree_hash + "\n")
    print(tree_hash)

if __name__ == '__main__':
    sys.exit(main())
