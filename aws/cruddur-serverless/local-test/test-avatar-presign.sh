#!/bin/bash

set -euo pipefail

# -------------------------------
# Configuration (EDIT THESE)
# -------------------------------
API_BASE_URL="https://mizxii4b39.execute-api.eu-west-2.amazonaws.com"
PRESIGN_PATH="/avatars/presign"
TEST_IMAGE_PATH="./sample2.png"
EXTENSION="png"
CONTENT_TYPE="image/png"



# ACCESS_TOKEN="${ACCESS_TOKEN:-}" # Either export ACCESS_TOKEN beforehand
# or paste it here for testing
ACCESS_TOKEN="eyJraWQiOiJpZTU4dFFoOHZhRHJjVzRLTjhDQTQyRGQxbW55dzFOaXNwa1dTY0lMU1gwPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI3NjMyYjJlNC02MDkxLTcwZDItMWQwMy03Mzk3OWNmN2UzMmIiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0yLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMl9Kd2k5VEhYM2IiLCJjbGllbnRfaWQiOiIxbHM1cDF2dTgzbTVhaHNlYWIzNnVmazZ2bSIsIm9yaWdpbl9qdGkiOiI1NmEyMGJiMi05NjcwLTRlZjktYmJkMS04MTNkODViNGNmYWYiLCJldmVudF9pZCI6IjkxOTM0YTE0LTIzMzctNDc2Yi1hZjc4LTU5YWQyMTVlY2VlNCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NjU2NzA2NjIsImV4cCI6MTc2NTgxMjg0MCwiaWF0IjoxNzY1ODA5MjQwLCJqdGkiOiIzM2NmNmQyNy1lNDAyLTRkYWMtOTYwMC03NTIyMmJiNjg5OWQiLCJ1c2VybmFtZSI6Ijc2MzJiMmU0LTYwOTEtNzBkMi0xZDAzLTczOTc5Y2Y3ZTMyYiJ9.hrxMSQYbdhIHLuRKH0HEyBRk3OWaMPyQzq9EsJnaiVkM3eYV46m4ECjoq81FhVZvdwwhhzoTcLTLsAPW7fPZo2KfzixUleVUHNPbWdQ_fBdIIIodQi0JaXT1jBasnpbR4vNuhSVQQSva0pkK5L8SAJZ0TTb-kcSpt1S85VLTikDKG_8fjAvdB82s8K9ExS0KD3Bor59vlkCZRIe7gprnbU6TLfiOoggZ1Gz1j7h6CqBg_N5GVb43nO25Wx_ItHDK-J7VG63lo4MOKtnXuVJD2eiwXjnqdHqg8ZgZHZm_ZkXvBCUUAM2qEbckOfw4nIlh1hpoFaXdgTWUgmXoCTr-bA"

# -------------------------------
# Validation
# -------------------------------
if [ -z "$ACCESS_TOKEN" ]; then
  echo "ERROR: ACCESS_TOKEN not set"
  echo "Run: export ACCESS_TOKEN=<cognito_access_token>"
  exit 1
fi

if [ ! -f "$TEST_IMAGE_PATH" ]; then
  echo "ERROR: Test image not found: $TEST_IMAGE_PATH"
  exit 1
fi

# -------------------------------
# Request presigned URL
# -------------------------------
echo "Requesting presigned URL..."
echo "POST ${API_BASE_URL}${PRESIGN_PATH}"

RESPONSE=$(curl --fail --show-error --silent --max-time 10 \
  -X POST \
  "${API_BASE_URL}${PRESIGN_PATH}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"extension\": \"${EXTENSION}\",
    \"content_type\": \"${CONTENT_TYPE}\"
  }"
)

echo "Presign response:"
echo "$RESPONSE"

# -------------------------------
# Parse response (jq required)
# -------------------------------
UPLOAD_URL=$(echo "$RESPONSE" | jq -r '.upload_url')
S3_KEY=$(echo "$RESPONSE" | jq -r '.key')

if [ -z "$UPLOAD_URL" ] || [ "$UPLOAD_URL" = "null" ]; then
  echo "ERROR: upload_url missing in response"
  exit 1
fi

if [ -z "$S3_KEY" ] || [ "$S3_KEY" = "null" ]; then
  echo "ERROR: key missing in response"
  exit 1
fi

echo "Presigned URL OK"
echo "S3 Key: $S3_KEY"

# -------------------------------
# Upload image using presigned URL
# -------------------------------
echo "Uploading image via presigned URL..."

curl --fail --show-error --silent --max-time 10 \
  -X PUT \
  -H "Content-Type: ${CONTENT_TYPE}" \
  --upload-file "$TEST_IMAGE_PATH" \
  "$UPLOAD_URL"

echo "Upload completed"

# -------------------------------
# Verify object exists in S3
# -------------------------------
BUCKET_NAME="assets.cruddur.jawid.me"

echo "Verifying upload:"
echo "s3://${BUCKET_NAME}/${S3_KEY}"

aws s3 ls "s3://${BUCKET_NAME}/${S3_KEY}" >/dev/null 2>&1

if [ $? -eq 0 ]; then
  echo "SUCCESS: Avatar uploaded successfully"
else
  echo "ERROR: Uploaded object not found in S3"
  exit 1
fi
