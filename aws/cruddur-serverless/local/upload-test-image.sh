#!/bin/bash

# -------------------------------
# Configuration
# -------------------------------
https://assets.cruddur.jawid.me/avatar/original/sample2.png
BUCKET_NAME="assets.cruddur.jawid.me"
INPUT_PREFIX="avatar/original"
TEST_IMAGE_PATH="./sample2.png"

# Check if file exists
if [ ! -f "$TEST_IMAGE_PATH" ]; then
    echo "Error: Test image not found at $TEST_IMAGE_PATH"
    exit 1
fi

# Extract filename
FILENAME=$(basename "$TEST_IMAGE_PATH")

# Full S3 key
S3_KEY="$INPUT_PREFIX/$FILENAME"

# Upload file to S3
# echo "Uploading $TEST_IMAGE_PATH to s3://$BUCKET_NAME/$S3_KEY ..."
# aws s3 cp "$TEST_IMAGE_PATH" "s3://$BUCKET_NAME/$S3_KEY"

echo "Uploading $TEST_IMAGE_PATH to CDN instead of s3://$BUCKET_NAME/$S3_KEY ..."
aws s3 cp "$TEST_IMAGE_PATH" "s3://$BUCKET_NAME/$S3_KEY"

if [ $? -eq 0 ]; then
    echo "Upload successful. Lambda should trigger automatically."
else
    echo "Upload failed!"
fi
