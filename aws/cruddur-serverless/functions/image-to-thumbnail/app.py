import os
import json
import boto3
import tempfile
from PIL import Image

# Try to import requests, but allow function to run even if it's missing
try:
    import requests
except Exception:
    requests = None

s3 = boto3.client("s3")
sns = boto3.client("sns")

BUCKET = os.environ["THUMBING_BUCKET_NAME"]
INPUT_PREFIX = os.environ["THUMBING_S3_FOLDER_INPUT"]
OUTPUT_PREFIX = os.environ["THUMBING_S3_FOLDER_OUTPUT"]
WEBHOOK_URL = os.environ["THUMBING_WEBHOOK_URL"]
# Topic ARN provided by CloudFormation
sns_arn = os.environ["THUMBING_TOPIC_ARN"]

def lambda_handler(event, context):
    print("Event:", event)

    for record in event["Records"]:
        key = record["s3"]["object"]["key"]

        if not key.startswith(INPUT_PREFIX):
            print("Skipping non-input key:", key)
            continue

        filename = key.split("/")[-1]
        base_name, _ = os.path.splitext(filename)
        output_filename = f"{base_name}.jpg"
        output_key = OUTPUT_PREFIX + output_filename

        # Download original
        with tempfile.NamedTemporaryFile(delete=False) as temp_in:
            s3.download_file(BUCKET, key, temp_in.name)
            input_path = temp_in.name

        try:
            # Create thumbnail using Pillow
            with Image.open(input_path) as img:
                img.thumbnail((256, 256), Image.Resampling.LANCZOS)

                # Convert RGBA (or other) to RGB so JPEG save works
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[-1])
                    img_out = background
                else:
                    img_out = img.convert("RGB")

                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_out:
                    img_out.save(temp_out.name, "JPEG")
                    output_path = temp_out.name

            # Upload thumbnail
            s3.upload_file(output_path, BUCKET, output_key)

            payload = {
                "original": key,
                "thumbnail": output_key
            }

            # Send webhook (only if requests is available)
            if requests is not None:
                try:
                    requests.post(WEBHOOK_URL, json=payload, timeout=3)
                except Exception as e:
                    print("Webhook failed:", e)
            else:
                print("Skipping webhook: `requests` not available in runtime.")

            # Publish SNS event
            sns.publish(
                TopicArn=sns_arn,
                Message=json.dumps(payload),
                Subject="Thumbnail Generated"
            )
        finally:
            # Cleanup temp files
            try:
                os.unlink(input_path)
            except Exception:
                pass
            try:
                os.unlink(output_path)
            except Exception:
                pass

    return {"status": "ok"}