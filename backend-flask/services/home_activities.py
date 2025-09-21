from datetime import datetime, timedelta, timezone
from opentelemetry import trace
from lib.db import pool

tracer = trace.get_tracer("home.activities.service") 

class HomeActivities:
  def run(user_claims=None):
    with tracer.start_as_current_span("home-activities-all-mock-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())
      
      with pool.connection() as conn:
        with conn.cursor() as cur:
          # Get main activities (not replies)
          cur.execute("""
            SELECT 
              activities.uuid,
              users.display_name,
              users.handle,
              activities.message,
              activities.replies_count,
              activities.reposts_count,
              activities.likes_count,
              activities.expires_at,
              activities.created_at
            FROM public.activities
            LEFT JOIN public.users ON users.uuid = activities.user_uuid
            WHERE activities.reply_to_activity_uuid IS NULL
            ORDER BY activities.created_at DESC
          """)
          main_activities = cur.fetchall()
          
          # Get all replies
          cur.execute("""
            SELECT 
              activities.uuid,
              users.display_name,
              users.handle,
              activities.message,
              activities.likes_count,
              activities.replies_count,
              activities.reposts_count,
              activities.reply_to_activity_uuid,
              activities.created_at
            FROM public.activities
            LEFT JOIN public.users ON users.uuid = activities.user_uuid
            WHERE activities.reply_to_activity_uuid IS NOT NULL
            ORDER BY activities.created_at DESC
          """)
          replies = cur.fetchall()
      
      # Group replies by parent activity
      replies_dict = {}
      for reply in replies:
        parent_uuid = str(reply[7])
        if parent_uuid not in replies_dict:
          replies_dict[parent_uuid] = []
        replies_dict[parent_uuid].append({
          'uuid': str(reply[0]),
          'reply_to_activity_uuid': parent_uuid,
          'handle': reply[2],
          'message': reply[3],
          'likes_count': reply[4],
          'replies_count': reply[5],
          'reposts_count': reply[6],
          'created_at': reply[8].isoformat()
        })
      
      # Build results with public activities
      results = []
      for activity in main_activities:
        activity_uuid = str(activity[0])
        activity_data = {
          'uuid': activity_uuid,
          'handle': activity[2],
          'message': activity[3],
          'created_at': activity[8].isoformat(),
          'expires_at': activity[7].isoformat() if activity[7] else None,
          'likes_count': activity[6],
          'replies_count': activity[4],
          'reposts_count': activity[5],
          'replies': replies_dict.get(activity_uuid, [])
        }
        
        # Show all activities if user is authenticated, otherwise filter
        if user_claims or activity[2] == 'andrewbrown':
          results.append(activity_data)
      
      span.set_attribute("app.results_length", len(results))
      return results
