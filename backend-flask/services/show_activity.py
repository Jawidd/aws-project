from lib.db import pool

class ShowActivity:
  """
  Fetch a single activity and its replies.
  """
  def run(activity_uuid, user_claims=None):
    current_user_uuid = None
    if user_claims and user_claims.get('sub'):
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(
            "SELECT uuid FROM public.users WHERE cognito_user_id = %s",
            (user_claims['sub'],)
          )
          row = cur.fetchone()
          if row:
            current_user_uuid = row[0]

    with pool.connection() as conn:
      with conn.cursor() as cur:
        # Fetch the primary activity
        cur.execute(
          """
          SELECT 
            activities.uuid,
            users.handle,
            COALESCE(users.full_name, users.preferred_username, users.handle) AS display_name,
            activities.message,
            activities.replies_count,
            activities.reposts_count,
            activities.likes_count,
            activities.expires_at,
            activities.created_at,
            activities.reply_to_activity_uuid,
            activities.user_uuid,
            users.avatar_url
          FROM public.activities
          LEFT JOIN public.users ON users.uuid = activities.user_uuid
          WHERE activities.uuid = %s
          """,
          (activity_uuid,)
        )
        activity_row = cur.fetchone()

        if not activity_row:
          return {'error': 'activity_not_found'}

        liked = False
        if current_user_uuid:
          cur.execute(
            "SELECT 1 FROM public.likes WHERE activity_uuid = %s AND user_uuid = %s",
            (activity_uuid, current_user_uuid)
          )
          liked = cur.fetchone() is not None

        activity = {
          'uuid': str(activity_row[0]),
          'handle': activity_row[1],
          'display_name': activity_row[2],
          'message': activity_row[3],
          'replies_count': activity_row[4] or 0,
          'reposts_count': activity_row[5] or 0,
          'likes_count': activity_row[6] or 0,
          'expires_at': activity_row[7].isoformat() if activity_row[7] else None,
          'created_at': activity_row[8].isoformat() if activity_row[8] else None,
          'reply_to_activity_uuid': str(activity_row[9]) if activity_row[9] else None,
          'liked': liked,
          'avatar_url': activity_row[11]
        }

        # Fetch replies for this activity
        cur.execute(
          """
          SELECT 
            activities.uuid,
            activities.reply_to_activity_uuid,
            users.handle,
            COALESCE(users.full_name, users.preferred_username, users.handle) AS display_name,
            activities.message,
            activities.replies_count,
            activities.reposts_count,
            activities.likes_count,
            activities.created_at,
            activities.user_uuid,
            users.avatar_url
          FROM public.activities
          LEFT JOIN public.users ON users.uuid = activities.user_uuid
          WHERE activities.reply_to_activity_uuid = %s
          ORDER BY activities.created_at ASC
          """,
          (activity_uuid,)
        )
        reply_rows = cur.fetchall()

        reply_ids = [row[0] for row in reply_rows]
        liked_reply_ids = set()
        if current_user_uuid and reply_ids:
          cur.execute(
            """
            SELECT activity_uuid 
            FROM public.likes 
            WHERE user_uuid = %s AND activity_uuid = ANY(%s)
            """,
            (current_user_uuid, reply_ids)
          )
          liked_reply_ids = {row[0] for row in cur.fetchall()}

        replies = []
        for reply in reply_rows:
          replies.append({
            'uuid': str(reply[0]),
            'reply_to_activity_uuid': str(reply[1]) if reply[1] else None,
            'handle': reply[2],
            'display_name': reply[3],
            'message': reply[4],
            'replies_count': reply[5] or 0,
            'reposts_count': reply[6] or 0,
            'likes_count': reply[7] or 0,
            'created_at': reply[8].isoformat() if reply[8] else None,
            'liked': reply[0] in liked_reply_ids,
            'avatar_url': reply[10]
          })

    return {
      'activity': activity,
      'replies': replies
    }
