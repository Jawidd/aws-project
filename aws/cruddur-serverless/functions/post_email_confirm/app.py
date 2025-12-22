import logging
import os

import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    conn = None
    try:
        attrs = event.get("request", {}).get("userAttributes", {})
        cognito_user_id = event.get("userName")

        email = attrs.get("email")
        preferred_username = attrs.get("preferred_username")
        full_name = attrs.get("name")

        handle = preferred_username or (email.split("@")[0] if email else "unknown")

        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.users (
                    preferred_username,
                    handle,
                    email,
                    cognito_user_id,
                    full_name
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
            """, (
                preferred_username,
                handle,
                email,
                cognito_user_id,
                full_name
            ))
            conn.commit()

        logger.info("User post-confirmation processed : %s", email)

    except Exception:
        logger.exception("Post-confirmation handler failed")
        raise
    finally:
        if conn:
            conn.close()

    return event
