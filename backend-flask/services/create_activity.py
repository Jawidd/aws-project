from datetime import datetime, timezone, timedelta
import uuid
from lib.db import pool

class CreateActivity:
  def run(message, ttl, user_claims=None):
    model = {
      'errors': None,
      'data': None
    }

    # Check if user is authenticated
    if not user_claims:
      model['errors'] = ['user_not_authenticated']
      return model

    now = datetime.now(timezone.utc).astimezone()

    if ttl == '30-days':
      ttl_offset = timedelta(days=30) 
    elif ttl == '7-days':
      ttl_offset = timedelta(days=7) 
    elif ttl == '3-days':
      ttl_offset = timedelta(days=3) 
    elif ttl == '1-day':
      ttl_offset = timedelta(days=1) 
    elif ttl == '12-hours':
      ttl_offset = timedelta(hours=12) 
    elif ttl == '3-hours':
      ttl_offset = timedelta(hours=3) 
    elif ttl == '1-hour':
      ttl_offset = timedelta(hours=1) 
    else:
      model['errors'] = ['ttl_blank']

    if message is None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 280:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      return model
    
    expires_at = now + ttl_offset
    activity_uuid = uuid.uuid4()
    
    try:
      with pool.connection() as conn:
        with conn.cursor() as cur:
          # Get user by cognito_user_id from JWT claims
          cognito_user_id = user_claims.get('sub')
          cur.execute("""
            SELECT uuid, handle, full_name, preferred_username, avatar_url 
            FROM public.users 
            WHERE cognito_user_id = %s
          """, (cognito_user_id,))
          user_result = cur.fetchone()
          
          if not user_result:
            model['errors'] = ['user_not_found']
            return model
          
          user_uuid, user_handle, full_name, preferred_username, avatar_url = user_result
          display_name = full_name or preferred_username or user_handle
          
          cur.execute("""
            INSERT INTO public.activities (uuid, user_uuid, message, expires_at)
            VALUES (%s, %s, %s, %s)
          """, (activity_uuid, user_uuid, message, expires_at))
          
          conn.commit()
          
    except Exception as e:
      model['errors'] = ['database_error']
      return model
    
    model['data'] = {
      'uuid': str(activity_uuid),
      'handle': user_handle,
      'display_name': display_name,
      'message': message,
      'replies_count': 0,
      'reposts_count': 0,
      'likes_count': 0,
      'created_at': now.isoformat(),
      'expires_at': expires_at.isoformat(),
      'liked': False,
      'avatar_url': avatar_url,
      'replies': []
    }
    return model
