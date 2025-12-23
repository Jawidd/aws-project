#!/usr/bin/env bash
set -euo pipefail

MAIN_BRANCH="main"
PROD_BRANCH="prod"

echo "🔄 Fetching latest refs..."
git fetch origin

echo "✅ Ensuring main is up to date..."
git checkout "$MAIN_BRANCH"
git pull origin "$MAIN_BRANCH"

echo "🚀 Promoting main → prod..."
git checkout "$PROD_BRANCH"
git reset --hard "origin/$MAIN_BRANCH"

echo "📦 Pushing prod (force update)..."
git push origin "$PROD_BRANCH" --force

echo "🔙 Switching back to main..."
git checkout "$MAIN_BRANCH"

echo "🎉 Release complete! prod is now identical to main."
