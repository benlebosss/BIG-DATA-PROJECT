#!/usr/bin/env bash
# Usage: scripts/protect_main.sh <owner>/<repo>   (needs `gh auth login` first)
# Requires a PR with 1 approving review before merging into main.
set -euo pipefail
REPO="$1"
gh api -X PUT "repos/$REPO/branches/main/protection" --input - <<JSON
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {"required_approving_review_count": 1},
  "restrictions": null
}
JSON
echo "main is now protected on $REPO"
