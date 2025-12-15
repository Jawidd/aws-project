import logging
import os
from lib.db import db

ASSETS_BASE_URL = os.getenv("ASSETS_BASE_URL", "https://assets.cruddur.jawid.me")


def build_public_url(key: str) -> str:
  base = ASSETS_BASE_URL.rstrip("/")
  clean_key = key.lstrip("/")
  return f"{base}/{clean_key}"


def extract_cognito_user_id(key: str) -> str:
  filename = key.split("/")[-1]
  if not filename:
    return None
  parts = filename.split(".")
  if len(parts) < 2:
    return None
  return parts[0]


class AvatarWebhook:
  @staticmethod
  def update_avatar(cognito_user_id: str, avatar_url: str):
    logging.info(f"Updating avatar for {cognito_user_id} -> {avatar_url}")
    sql = """
      UPDATE public.users
      SET avatar_url = %(avatar_url)s
      WHERE cognito_user_id = %(cognito_user_id)s
      RETURNING uuid, handle, full_name, bio, avatar_url
    """
    try:
      with db.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql, {
            'avatar_url': avatar_url,
            'cognito_user_id': cognito_user_id
          })
          result = cur.fetchone()
          conn.commit()

          if result:
            return {
              'errors': None,
              'data': {
                'uuid': str(result[0]),
                'handle': result[1],
                'display_name': result[2],
                'bio': result[3] or '',
                'avatar_url': result[4]
              }
            }

          return {
            'errors': ['user_not_found'],
            'data': None
          }
    except Exception as e:
      logging.error(f"AvatarWebhook.update_avatar failed: {str(e)}")
      return {
        'errors': [str(e)],
        'data': None
      }
