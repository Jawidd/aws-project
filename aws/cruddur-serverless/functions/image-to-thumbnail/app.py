import os
import json
import boto3
import tempfile
import time
from PIL import Image

s3 = boto3.client("s3")
sns = boto3.client("sns")

BUCKET = os.environ["THUMBING_BUCKET_NAME"]
INPUT_PREFIX = os.environ["THUMBING_S3_FOLDER_INPUT"]
OUTPUT_PREFIX = os.environ["THUMBING_S3_FOLDER_OUTPUT"]
TOPIC_ARN = os.environ["THUMBING_TOPIC_ARN"]


def delete_old_avatars(bucket, prefix, keep_key):
    """
    Deletes all processed avatars for a user except the newest one.
    """
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )

    for obj in response.get("Contents", []):
        key = obj["Key"]
        if key != keep_key:
            s3.delete_object(Bucket=bucket, Key=key)


def lambda_handler(event, context):
    for record in event["Records"]:
        key = record["s3"]["object"]["key"]

        # Only process original uploads
        if not key.startswith(INPUT_PREFIX):
            continue

        filename = key.split("/")[-1]
        base_name = filename.split(".")[0]

        # 🔑 cache-busting filename
        version = int(time.time())
        output_key = f"{OUTPUT_PREFIX}{base_name}_{version}.jpg"

        # Download original
        with tempfile.NamedTemporaryFile(delete=False) as temp_in:
            s3.download_file(BUCKET, key, temp_in.name)
            input_path = temp_in.name

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

            # 🔥 delete older avatars for this user
            user_prefix = f"{OUTPUT_PREFIX}{base_name}_"
            delete_old_avatars(BUCKET, user_prefix, output_key)

            # Publish SNS event
            sns.publish(
                TopicArn=TOPIC_ARN,
                Message=json.dumps({
                    "original": key,
                    "thumbnail": output_key
                }),
                Subject="AvatarThumbnailCreated"
            )

        finally:
            try:
                os.unlink(input_path)
            except Exception:
                pass
            try:
                os.unlink(output_path)
            except Exception:
                pass

    return {"status": "ok"}
