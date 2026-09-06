#!/usr/bin/env bash

# Helper script to remove a checked-in .venv from the repository index and commit the change
# Usage: ./scripts/remove_venv.sh

set -euo pipefail

if [ ! -d ".venv" ]; then
  echo ".venv directory does not exist locally. Nothing to do." >&2
  exit 0
fi

echo "Removing .venv from git index (keeps local files)..."

git rm -r --cached .venv

git commit -m "chore: remove checked-in virtualenv (.venv)"

echo "Committed removal of .venv. Push the branch to remote (example):"

echo "  git push origin faang/initial-hardening"

echo "Note: This script does not rewrite history. If you need to remove .venv from history, use BFG or git filter-repo with care."
