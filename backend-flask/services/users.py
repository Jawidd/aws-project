# /backend-flask/services/users.py
from lib.db import pool
from flask import current_app

class UsersService:
    @staticmethod
    def get_user_by_cognito_id(cognito_id: str):
        """
        Fetch user from PostgreSQL by their Cognito UUID.
        Returns a dictionary with user info or None if not found.
        """
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT uuid, preferred_username, handle, email, cognito_user_id, bio, avatar_url
                        FROM public.users
                        WHERE cognito_user_id = %s
                        LIMIT 1
                    """, (cognito_id,))
                    user = cur.fetchone()
                    if not user:
                        return None
                    return {
                        "uuid": str(user[0]),
                        "preferred_username": user[1],
                        "handle": user[2],
                        "email": user[3],
                        "cognito_user_id": user[4],
                        "bio": user[5],
                        "avatar_url": user[6]
                    }
        except Exception as e:
            current_app.logger.error(f"Error fetching user {cognito_id}: {e}", exc_info=True)
            return None
