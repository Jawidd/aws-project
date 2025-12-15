import json
import os
import boto3

s3 = boto3.client("s3")

BUCKET = os.environ["AVATAR_UPLOAD_BUCKET"]
PREFIX = os.getenv("AVATAR_UPLOAD_PREFIX", "avatar/original/")
URL_TTL = int(os.getenv("PRESIGN_URL_TTL_SECONDS", "300"))

if not PREFIX.endswith("/"):
    PREFIX += "/"

def lambda_handler(event, context):
    claims = (
        event.get("requestContext", {})
        .get("authorizer", {})
        .get("jwt", {})
        .get("claims", {})
    )

    cognito_sub = claims.get("sub")
    if not cognito_sub:
        return {"statusCode": 401, "body": json.dumps({"error": "unauthorized"})}

    body = json.loads(event.get("body") or "{}")

    extension = (body.get("extension") or "jpg").lstrip(".").lower()
    content_type = body.get("content_type")

    object_key = f"{PREFIX}{cognito_sub}.{extension}"

    params = {"Bucket": BUCKET, "Key": object_key}
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
