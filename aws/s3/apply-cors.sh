#!/usr/bin/env bash
set -euo pipefail

BUCKET="${1:-assets.cruddur.jawid.me}"
CORS_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/cors-assets.json"

echo "Applying CORS from ${CORS_FILE} to bucket ${BUCKET}"
aws s3api put-bucket-cors \
  --bucket "${BUCKET}" \
  --cors-configuration "file://${CORS_FILE}"

echo "Done."
