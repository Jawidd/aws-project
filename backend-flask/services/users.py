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
                        SELECT uuid, preferred_username, full_name, handle, email, cognito_user_id, bio, avatar_url
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
                        "full_name": user[2],
                        "handle": user[3],
                        "email": user[4],
                        "cognito_user_id": user[5],
                        "bio": user[6],
                        "avatar_url": user[7]
                    }
        except Exception as e:
            current_app.logger.error(f"Error fetching user {cognito_id}: {e}", exc_info=True)
            return None

    @staticmethod
    def get_user_by_handle(handle: str):
        """
        Fetch user from PostgreSQL by their handle.
        Returns a dictionary with user info or None if not found.
        """
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT uuid, preferred_username, full_name, handle, email, cognito_user_id, bio, avatar_url
                        FROM public.users
                        WHERE handle = %s
                        LIMIT 1
                    """, (handle,))
                    user = cur.fetchone()
                    if not user:
                        return None
                    return {
                        "uuid": str(user[0]),
                        "preferred_username": user[1],
                        "full_name": user[2],
                        "handle": user[3],
                        "email": user[4],
                        "cognito_user_id": user[5],
                        "bio": user[6],
                        "avatar_url": user[7]
                    }
        except Exception as e:
            current_app.logger.error(f"Error fetching user by handle {handle}: {e}", exc_info=True)
            return None

    @staticmethod
    def get_user_by_uuid(user_uuid: str):
        """
        Fetch user from PostgreSQL by their UUID.
        Returns a dictionary with user info or None if not found.
        """
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT uuid, preferred_username, full_name, handle, email, cognito_user_id, bio, avatar_url
                        FROM public.users
                        WHERE uuid = %s
                        LIMIT 1
                    """, (user_uuid,))
                    user = cur.fetchone()
                    if not user:
                        return None
                    return {
                        "uuid": str(user[0]),
                        "preferred_username": user[1],
                        "full_name": user[2],
                        "handle": user[3],
                        "email": user[4],
                        "cognito_user_id": user[5],
                        "bio": user[6],
                        "avatar_url": user[7]
                    }
        except Exception as e:
            current_app.logger.error(f"Error fetching user by UUID {user_uuid}: {e}", exc_info=True)
            return None

    @staticmethod
    def get_users_without_conversations(current_user_uuid: str, existing_uuids=None):
        """
        Get users that current user hasn't had conversations with.
        """
        if existing_uuids is None:
            existing_uuids = []
            
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    if existing_uuids:
                        placeholders = ','.join(['%s'] * len(existing_uuids))
                        query = f"""
                            SELECT uuid, preferred_username, full_name, handle, email, bio, avatar_url
                            FROM public.users
                            WHERE uuid != %s AND uuid NOT IN ({placeholders})
                            ORDER BY full_name, handle
                            LIMIT 20
                        """
                        params = [current_user_uuid] + existing_uuids
                    else:
                        query = """
                            SELECT uuid, preferred_username, full_name, handle, email, bio, avatar_url
                            FROM public.users
                            WHERE uuid != %s
                            ORDER BY full_name, handle
                            LIMIT 20
                        """
                        params = [current_user_uuid]
                    
                    cur.execute(query, params)
                    users = cur.fetchall()
                    return [{
                        "uuid": str(user[0]),
                        "preferred_username": user[1],
                        "full_name": user[2],
                        "handle": user[3],
                        "email": user[4],
                        "bio": user[5],
                        "avatar_url": user[6]
                    } for user in users]
        except Exception as e:
            current_app.logger.error(f"Error fetching users: {e}", exc_info=True)
            return []
