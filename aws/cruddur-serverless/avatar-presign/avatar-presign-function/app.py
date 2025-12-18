import json
import os

import boto3

s3 = boto3.client("s3")

BUCKET = os.environ["AVATAR_UPLOAD_BUCKET"]
PREFIX = os.getenv("AVATAR_UPLOAD_PREFIX", "avatar/original/")
URL_TTL = int(os.getenv("PRESIGN_URL_TTL_SECONDS", "300"))

# Ensure folder-style prefix
if not PREFIX.endswith("/"):
    PREFIX += "/"


def lambda_handler(event, context):
    request_context = event.get("requestContext", {})
    jwt = request_context.get("authorizer", {}).get("jwt", {})
    claims = jwt.get("claims", {}) or {}

    user_sub = claims.get("sub")
    if not user_sub:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "unauthorized"})
        }

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "invalid json body"})
        }

    file_ext = (body.get("extension") or "jpg").lstrip(".").lower()
    content_type = body.get("content_type")

    # Predictable object key simplifies cleanup later
    object_key = f"{PREFIX}{user_sub}.{file_ext}"

    params = {
        "Bucket": BUCKET,
        "Key": object_key
    }

    if content_type:
        params["ContentType"] = content_type

    upload_url = s3.generate_presigned_url(
        "put_object",
        Params=params,
        ExpiresIn=URL_TTL
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "upload_url": upload_url,
            "key": object_key
        })
    }
