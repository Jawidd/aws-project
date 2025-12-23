import json
import os

import boto3

s3 = boto3.client("s3")

BUCKET = os.environ["AVATAR_UPLOAD_BUCKET"]
AVATAR_PREFIX = os.getenv("AVATAR_UPLOAD_PREFIX", "avatar/original/")
COVER_PREFIX = "cover-photos/"
URL_TTL = int(os.getenv("PRESIGN_URL_TTL_SECONDS", "300"))

# Ensure folder-style prefixes
if not AVATAR_PREFIX.endswith("/"):
    AVATAR_PREFIX += "/"
if not COVER_PREFIX.endswith("/"):
    COVER_PREFIX += "/"


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
    upload_type = body.get("type", "avatar").lower()

    # Choose prefix based on upload type
    prefix = COVER_PREFIX if upload_type == "cover" else AVATAR_PREFIX
    
    # Predictable object key simplifies cleanup later
    object_key = f"{prefix}{user_sub}.{file_ext}"

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
