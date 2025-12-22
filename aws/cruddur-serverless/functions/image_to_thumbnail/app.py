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


def list_keys(bucket, prefix):
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            yield obj["Key"]


def delete_keys(bucket, keys):
    keys = list(keys)
    for i in range(0, len(keys), 1000):
        chunk = [{"Key": k} for k in keys[i:i + 1000]]
        s3.delete_objects(Bucket=bucket, Delete={"Objects": chunk})


def clean_all_user_files(user_id):
    """Delete ALL existing files for a user before processing new upload"""
    # Clean processed files
    processed_prefix = f"{OUTPUT_PREFIX}{user_id}_"
    processed_keys = list(list_keys(BUCKET, processed_prefix))
    
    # Clean original files  
    original_prefix = f"{INPUT_PREFIX}{user_id}"
    original_keys = list(list_keys(BUCKET, original_prefix))
    
    all_to_delete = processed_keys + original_keys
    if all_to_delete:
        delete_keys(BUCKET, all_to_delete)
        logger.info("Deleted %s existing files for user %s", len(all_to_delete), user_id)


def publish_avatar_event(original_key, thumbnail_key):
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
        logger.exception("SNS publish failed")
        return False


def invoke_consumer_fallback(original_key, thumbnail_key):
    if not CONSUMER_ARN:
        return False

    payload = {
        "Records": [{
            "Sns": {
                "Message": json.dumps({
                    "original": original_key,
                    "thumbnail": thumbnail_key
                })
            }
        }]
    }

    try:
        lambda_client.invoke(
            FunctionName=CONSUMER_ARN,
            InvocationType="Event",
            Payload=json.dumps(payload).encode("utf-8")
        )
        logger.info("Invoked avatar-db-consumer as fallback")
        return True
    except Exception:
        logger.exception("Fallback invoke failed")
        return False


def lambda_handler(event, context):
    for record in event.get("Records", []):
        s3_info = record.get("s3", {})
        obj = s3_info.get("object", {})
        original_key = obj.get("key")

        if not original_key or not original_key.startswith(INPUT_PREFIX):
            continue

        filename = original_key.split("/")[-1]
        user_id = filename.split(".")[0]

        # Clean up ALL existing files for this user FIRST
        clean_all_user_files(user_id)

        version = int(time.time())
        output_key = f"{OUTPUT_PREFIX}{user_id}_{version}.jpg"

        input_path = None
        output_path = None

        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                s3.download_file(BUCKET, original_key, tmp.name)
                input_path = tmp.name

            with Image.open(input_path) as img:
                img.thumbnail((256, 256), Image.Resampling.LANCZOS)
                img = img.convert("RGB")

                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    img.save(tmp.name, "JPEG")
                    output_path = tmp.name

            s3.upload_file(output_path, BUCKET, output_key)

            if not publish_avatar_event(original_key, output_key):
                invoke_consumer_fallback(original_key, output_key)

        finally:
            for path in (input_path, output_path):
                try:
                    if path and os.path.exists(path):
                        os.unlink(path)
                except Exception:
                    pass

    return {"status": "ok"}
