import json
import logging
import os
import tempfile
import time

import boto3
from PIL import Image

s3 = boto3.client("s3")
sns = boto3.client("sns")
lambda_client = boto3.client("lambda")

BUCKET = os.environ["THUMBING_BUCKET_NAME"]
INPUT_PREFIX = os.environ["THUMBING_S3_FOLDER_INPUT"].rstrip("/") + "/"
OUTPUT_PREFIX = os.environ["THUMBING_S3_FOLDER_OUTPUT"].rstrip("/") + "/"
TOPIC_ARN = os.environ["THUMBING_TOPIC_ARN"]
CONSUMER_ARN = os.getenv("AVATAR_DB_CONSUMER_ARN")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def list_keys(bucket: str, prefix: str):
    # Walk all keys under a prefix (S3 pagination handles big lists)
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            yield obj["Key"]


def delete_keys(bucket: str, keys):
    # Keep it simple: delete in small batches so we don't blow the limit
    keys = list(keys)
    for i in range(0, len(keys), 1000):
        chunk = [{"Key": k} for k in keys[i:i + 1000]]
        s3.delete_objects(Bucket=bucket, Delete={"Objects": chunk})


def clean_user_processed(base_name: str, keep_key: str):
    # Only leave the latest processed avatar around for this user
    prefix = f"{OUTPUT_PREFIX}{base_name}_"
    to_delete = [k for k in list_keys(BUCKET, prefix) if k != keep_key]
    if to_delete:
        delete_keys(BUCKET, to_delete)
        logger.info("Deleted %s old processed avatars for %s", len(to_delete), base_name)


def clean_user_originals(base_name: str, keep_key: str):
    # Clean up earlier originals regardless of extension
    prefix = f"{INPUT_PREFIX}{base_name}"
    to_delete = [k for k in list_keys(BUCKET, prefix) if k != keep_key]
    if to_delete:
        delete_keys(BUCKET, to_delete)
        logger.info("Deleted %s old original uploads for %s", len(to_delete), base_name)


def publish_avatar_event(original_key: str, thumbnail_key: str) -> bool:
    # Normal path: let SNS fan out the DB update
    try:
        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=json.dumps({
                "original": original_key,
                "thumbnail": thumbnail_key
            }),
            Subject="AvatarThumbnailCreated"
        )
        return True
    except Exception:
        logger.exception("Failed to publish avatar event to SNS")
        return False


def invoke_consumer_fallback(original_key: str, thumbnail_key: str) -> bool:
    # If SNS publish flakes, poke the consumer directly with the same shape
    if not CONSUMER_ARN:
        return False

    payload = {
        "Records": [
            {
                "Sns": {
                    "Message": json.dumps({
                        "original": original_key,
                        "thumbnail": thumbnail_key
                    })
                }
            }
        ]
    }

    try:
        lambda_client.invoke(
            FunctionName=CONSUMER_ARN,
            InvocationType="Event",
            Payload=json.dumps(payload).encode("utf-8")
        )
        logger.info("Invoked avatar-db-consumer directly as fallback")
        return True
    except Exception:
        logger.exception("Fallback invoke of avatar-db-consumer failed")
        return False


def lambda_handler(event, context):
    for record in event["Records"]:
        original_key = record["s3"]["object"]["key"]

        # Only process original uploads
        if not original_key.startswith(INPUT_PREFIX):
            continue

        filename = original_key.split("/")[-1]
        user_stub = filename.split(".")[0]  # cognito id portion

        # 🔑 cache-busting filename
        version_stamp = int(time.time())
        output_key = f"{OUTPUT_PREFIX}{user_stub}_{version_stamp}.jpg"

        # Download original
        with tempfile.NamedTemporaryFile(delete=False) as temp_in:
            s3.download_file(BUCKET, original_key, temp_in.name)
            input_path = temp_in.name
        output_path = None

        try:
            # Create thumbnail
            with Image.open(input_path) as img:
                img.thumbnail((256, 256), Image.Resampling.LANCZOS)
                img = img.convert("RGB")

                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_out:
                    img.save(temp_out.name, "JPEG")
                    output_path = temp_out.name

            # Upload thumbnail
            s3.upload_file(output_path, BUCKET, output_key)

            # 🔥 enforce single processed + single original per user
            clean_user_processed(user_stub, output_key)
            clean_user_originals(user_stub, original_key)

            # Publish SNS event, with a direct Lambda fallback if publish fails
            published = publish_avatar_event(original_key, output_key)
            if not published:
                invoked = invoke_consumer_fallback(original_key, output_key)
                if not invoked:
                    logger.error("Avatar DB update not triggered (SNS publish failed and fallback invoke failed)")

        finally:
            try:
                if input_path and os.path.exists(input_path):
                    os.unlink(input_path)
            except Exception:
                pass
            try:
                if output_path and os.path.exists(output_path):
                    os.unlink(output_path)
            except Exception:
                pass

    return {"status": "ok"}
