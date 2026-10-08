#!/usr/bin/env bash
# Run once from the project folder, after creating an EMPTY repo on GitHub.
# Usage: scripts/init_repo.sh git@github.com:<owner>/<repo>.git
set -euo pipefail
git init -b main
git commit --allow-empty -m "Initial commit"
git remote add origin "$1"
git push -u origin main
git checkout -b feature/setup
git add -A
git commit -m "Add project scaffolding: docker, scripts, docs, structure"
git push -u origin feature/setup
echo "Now open a PR feature/setup -> main on GitHub and ask your teammate to review."
