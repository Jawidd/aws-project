#!/bin/bash

# -------------------------------
# Configuration
# -------------------------------
BUCKET_NAME="assets.cruddur.jawid.me"
INPUT_PREFIX="avatar/original"
OUTPUT_PREFIX="avatar/processed"
TEST_IMAGE_PATH="./sample.jpg"
LOCAL_OUTPUT_DIR="./processed"

# -------------------------------
# Validation
# -------------------------------
if [ ! -f "$TEST_IMAGE_PATH" ]; then
    echo "Error: Test image not found at $TEST_IMAGE_PATH"
    exit 1
fi

# Create local output directory if missing
mkdir -p "$LOCAL_OUTPUT_DIR"

# Extract filename (sample2.png)
FILENAME=$(basename "$TEST_IMAGE_PATH")

# Extract base name (sample2)
BASENAME="${FILENAME%.*}"

# Processed filename (Lambda always outputs JPG)
PROCESSED_FILENAME="${BASENAME}.jpg"

# S3 keys
S3_INPUT_KEY="$INPUT_PREFIX/$FILENAME"
S3_OUTPUT_KEY="$OUTPUT_PREFIX/$PROCESSED_FILENAME"

# Local output path (KEEP NAME)
LOCAL_OUTPUT_PATH="$LOCAL_OUTPUT_DIR/$PROCESSED_FILENAME"

# -------------------------------
# Upload original image
# -------------------------------
echo "Uploading $TEST_IMAGE_PATH to s3://$BUCKET_NAME/$S3_INPUT_KEY ..."
aws s3 cp "$TEST_IMAGE_PATH" "s3://$BUCKET_NAME/$S3_INPUT_KEY"

if [ $? -ne 0 ]; then
    echo "Upload failed!"
    exit 1
fi

echo "Upload successful. Waiting for thumbnail generation..."

# -------------------------------
# Wait for Lambda processing
# -------------------------------
ATTEMPTS=5
SLEEP_SECONDS=3

for i in $(seq 1 $ATTEMPTS); do
    echo "Checking for processed image (attempt $i/$ATTEMPTS)..."
    aws s3 ls "s3://$BUCKET_NAME/$S3_OUTPUT_KEY" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Processed image found!"
        break
    fi
    sleep $SLEEP_SECONDS
done

# Final check
aws s3 ls "s3://$BUCKET_NAME/$S3_OUTPUT_KEY" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Processed image not found after waiting."
    exit 1
fi

# -------------------------------
# Download processed image (KEEP NAME)
# -------------------------------
echo "Downloading processed image to $LOCAL_OUTPUT_PATH ..."
aws s3 cp "s3://$BUCKET_NAME/$S3_OUTPUT_KEY" "$LOCAL_OUTPUT_PATH"

if [ $? -eq 0 ]; then
    echo "Download complete: $LOCAL_OUTPUT_PATH"
else
