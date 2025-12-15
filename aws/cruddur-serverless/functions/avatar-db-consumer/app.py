import json
import logging
import os
import psycopg2
from urllib.parse import urlparse

DATABASE_URL = os.getenv("DATABASE_URL")
ASSETS_BASE_URL = os.getenv("ASSETS_BASE_URL")


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL not set")

    result = urlparse(DATABASE_URL)

    return psycopg2.connect(
        host=result.hostname,
        port=result.port,
        dbname=result.path.lstrip("/"),
        user=result.username,
        password=result.password,
        sslmode="require"
    )


def extract_cognito_user_id(key: str):
    """
    Extracts cognito user id from:
    avatar/processed/<cognito_id>_<timestamp>.jpg
    """
    filename = key.split("/")[-1]
    name = filename.split(".")[0]
    return name.split("_")[0]


def build_public_url(key: str):
    return f"{ASSETS_BASE_URL.rstrip('/')}/{key.lstrip('/')}"


def update_avatar(cognito_user_id, avatar_url):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE public.users
                SET avatar_url = %s
                WHERE cognito_user_id = %s
            """, (avatar_url, cognito_user_id))
            conn.commit()
    finally:
        conn.close()


def lambda_handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["Sns"]["Message"])
        thumbnail_key = message.get("thumbnail")

        if not thumbnail_key:
            logging.warning("Missing thumbnail key")
            continue

        cognito_user_id = extract_cognito_user_id(thumbnail_key)
        if not cognito_user_id:
            logging.warning("Invalid thumbnail key: %s", thumbnail_key)
            continue

        avatar_url = build_public_url(thumbnail_key)
        logging.info("Updating avatar %s -> %s", cognito_user_id, avatar_url)

        update_avatar(cognito_user_id, avatar_url)

    return {"status": "ok"}
