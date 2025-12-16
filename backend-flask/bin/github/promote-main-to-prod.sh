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

echo "🔍 Finding pull request number..."
PR_NUMBER=$(gh pr list \
  --base "$BASE_BRANCH" \
  --head "$HEAD_BRANCH" \
  --state open \
  | awk 'NR==1 {print $1}')

if [ -z "$PR_NUMBER" ]; then
  echo "❌ Failed to find the pull request"
  exit 1
fi

echo "✅ Found PR #$PR_NUMBER"

echo "👍 Approving pull request..."
gh pr review "$PR_NUMBER" --approve

echo "🔀 Merging pull request..."
gh pr merge "$PR_NUMBER" --squash --delete-branch=false

echo "🎉 Promotion from main → prod completed successfully"
