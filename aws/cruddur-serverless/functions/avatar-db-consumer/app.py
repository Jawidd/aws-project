import json
import logging
import os
import time
from urllib.parse import urlparse

import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")
ASSETS_BASE_URL = os.getenv("ASSETS_BASE_URL")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
    # avatar/processed/<cognito_id>_<timestamp>.jpg -> cognito_id
    filename = key.split("/")[-1]
    name = filename.split(".")[0]
    return name.split("_")[0]


def build_public_url(key: str):
    return f"{ASSETS_BASE_URL.rstrip('/')}/{key.lstrip('/')}"


def update_avatar(cognito_user_id, avatar_url):
    # Keep trying a couple times in case the DB is momentarily unhappy
    max_attempts = 3
    retry_pause = 0.3

    for attempt in range(max_attempts):
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE public.users
                    SET avatar_url = %s
                    WHERE cognito_user_id = %s
                """, (avatar_url, cognito_user_id))
                conn.commit()
            logger.info("Avatar updated for %s", cognito_user_id)
            return
        except Exception as e:
            logger.warning("Update attempt %s failed for %s: %s", attempt + 1, cognito_user_id, e)
            if attempt == max_attempts - 1:
                raise
            time.sleep(retry_pause * (attempt + 1))
        finally:
            if conn:
                conn.close()


def lambda_handler(event, context):
    for record in event["Records"]:
        message_raw = record["Sns"]["Message"]
        message = json.loads(message_raw)
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
