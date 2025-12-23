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

    parsed = urlparse(DATABASE_URL)

    return psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        dbname=parsed.path.lstrip("/"),
        user=parsed.username,
        password=parsed.password,
        sslmode="require"
    )


def extract_cognito_user_id(key: str):
    # Handle both avatar and cover photo keys
    # avatar/processed/<cognito_id>_<timestamp>.jpg
    # cover-photos/<cognito_id>.jpg
    filename = key.split("/")[-1]
    base = filename.split(".")[0]
    
    # For cover photos, the filename is just the cognito_id
    if key.startswith("cover-photos/"):
        return base
    
    # For avatars, extract from timestamped filename
    return base.split("_")[0]


def build_public_url(key: str):
    return f"{ASSETS_BASE_URL.rstrip('/')}/{key.lstrip('/')}"


def update_avatar(cognito_user_id, avatar_url):
    max_attempts = 3
    backoff = 0.3

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
            logger.warning(
                "Update attempt %s failed for %s: %s",
                attempt + 1,
                cognito_user_id,
                e
            )
            if attempt == max_attempts - 1:
                raise
            time.sleep(backoff * (attempt + 1))
        finally:
            if conn:
                conn.close()


def update_cover_image(cognito_user_id, cover_url):
    max_attempts = 3
    backoff = 0.3

    for attempt in range(max_attempts):
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE public.users
                    SET cover_image_url = %s
                    WHERE cognito_user_id = %s
                """, (cover_url, cognito_user_id))
                conn.commit()
            logger.info("Cover image updated for %s", cognito_user_id)
            return
        except Exception as e:
            logger.warning(
                "Cover update attempt %s failed for %s: %s",
                attempt + 1,
                cognito_user_id,
                e
            )
            if attempt == max_attempts - 1:
                raise
            time.sleep(backoff * (attempt + 1))
        finally:
            if conn:
                conn.close()


def lambda_handler(event, context):
    for record in event.get("Records", []):
        # Handle both SNS events (for avatars) and direct S3 events (for cover photos)
        if "Sns" in record:
            # Avatar processing via SNS
            message_raw = record.get("Sns", {}).get("Message")
            if not message_raw:
                continue

            message = json.loads(message_raw)
            thumbnail_key = message.get("thumbnail")

            if not thumbnail_key:
                logger.warning("Missing thumbnail key")
                continue

            cognito_user_id = extract_cognito_user_id(thumbnail_key)
            if not cognito_user_id:
                logger.warning("Invalid thumbnail key: %s", thumbnail_key)
                continue

            avatar_url = build_public_url(thumbnail_key)
            logger.info("Updating avatar %s -> %s", cognito_user_id, avatar_url)
            update_avatar(cognito_user_id, avatar_url)
            
        elif "s3" in record:
            # Direct S3 event for cover photos
            s3_info = record.get("s3", {})
            obj = s3_info.get("object", {})
            cover_key = obj.get("key")
            
            if not cover_key or not cover_key.startswith("cover-photos/"):
                continue
                
            cognito_user_id = extract_cognito_user_id(cover_key)
            if not cognito_user_id:
                logger.warning("Invalid cover photo key: %s", cover_key)
                continue
                
            cover_url = build_public_url(cover_key)
            logger.info("Updating cover image %s -> %s", cognito_user_id, cover_url)
            update_cover_image(cognito_user_id, cover_url)

    return {"status": "ok"}
