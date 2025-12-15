#!/usr/bin/env bash
set -euo pipefail

# -----------------------------
# Config
# -----------------------------
BUCKET_NAME="assets.cruddur.jawid.me"
CLOUDFRONT_DIST_ID="E8PVS5207B19"
POLICY_FILE="bucket-policy.json"

# -----------------------------
# Get AWS Account ID
# -----------------------------
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "AWS Account ID: $AWS_ACCOUNT_ID"
echo "CloudFront Distribution ID: $CLOUDFRONT_DIST_ID"
echo "Bucket: $BUCKET_NAME"
echo

# -----------------------------
# Create bucket policy
# -----------------------------
cat > $POLICY_FILE <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontReadOnly",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudfront.amazonaws.com"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::$BUCKET_NAME/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceArn": "arn:aws:cloudfront::$AWS_ACCOUNT_ID:distribution/$CLOUDFRONT_DIST_ID"
        }
      }
    }
  ]
}
EOF

echo "Bucket policy written to $POLICY_FILE"
echo

# -----------------------------
# Apply bucket policy
# -----------------------------
echo "Applying bucket policy..."
aws s3api put-bucket-policy \
  --bucket "$BUCKET_NAME" \
  --policy "file://$POLICY_FILE"

echo "Bucket policy applied successfully."
echo

# -----------------------------
# Verify
# -----------------------------
echo "Verifying bucket policy..."
aws s3api get-bucket-policy \
  --bucket "$BUCKET_NAME" \
  --query Policy \
  --output text

echo
echo "✅ CloudFront can now read from the bucket"
echo "🌍 Test URL:"
echo "https://assets.cruddur.jawid.me/avatar/processed/<filename>.jpg"
