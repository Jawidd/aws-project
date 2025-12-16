#!/usr/bin/env bash
set -euo pipefail

BASE_BRANCH="prod"
HEAD_BRANCH="main"
TITLE="Promote main to prod"
BODY="Deploying changes from main to prod"

echo "🔄 Updating local branches..."
git checkout "$HEAD_BRANCH"
git pull origin "$HEAD_BRANCH"

echo "🚀 Creating pull request..."
gh pr create \
  --base "$BASE_BRANCH" \
  --head "$HEAD_BRANCH" \
  --title "$TITLE" \
  --body "$BODY"

echo "ℹ️ Pull request created. Waiting for external approval."
