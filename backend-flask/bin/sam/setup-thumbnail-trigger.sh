#!/usr/bin/env bash
set -e

# -------------------------------
# Config (adjust if needed)
# -------------------------------
REGION="eu-west-2"
ACCOUNT_ID="225442939245"

BUCKET_NAME="assets.cruddur.jawid.me"
LAMBDA_NAME="image-to-thumbnail"
PREFIX_FILTER="avatar/original/"
STATEMENT_ID="s3-invoke-thumbnail"

# -------------------------------
# Get Lambda ARN
# -------------------------------
echo "Fetching Lambda ARN for ${LAMBDA_NAME}..."

LAMBDA_ARN=$(aws lambda get-function \
  --function-name "${LAMBDA_NAME}" \
  --region "${REGION}" \
  --query 'Configuration.FunctionArn' \
  --output text)

echo "Lambda ARN: ${LAMBDA_ARN}"

# -------------------------------
# Add permission (ignore if exists)
# -------------------------------
echo "Adding S3 invoke permission to Lambda..."

aws lambda add-permission \
  --function-name "${LAMBDA_NAME}" \
  --statement-id "${STATEMENT_ID}" \
  --action "lambda:InvokeFunction" \
  --principal s3.amazonaws.com \
  --source-arn "arn:aws:s3:::${BUCKET_NAME}" \
  --region "${REGION}" \
  2>/dev/null || echo "Permission already exists, skipping"

# -------------------------------
# Configure S3 notification
# -------------------------------
echo "Configuring S3 bucket notification..."

aws s3api put-bucket-notification-configuration \
  --bucket "${BUCKET_NAME}" \
  --notification-configuration "{
    \"LambdaFunctionConfigurations\": [
      {
        \"LambdaFunctionArn\": \"${LAMBDA_ARN}\",
        \"Events\": [\"s3:ObjectCreated:*\"],
        \"Filter\": {
          \"Key\": {
            \"FilterRules\": [
              { \"Name\": \"prefix\", \"Value\": \"${PREFIX_FILTER}\" }
            ]
          }
        }
      }
    ]
  }"

echo "✅ Thumbnail trigger setup complete"
