import uuid
from datetime import datetime, timedelta, timezone
from lib.db import pool

class CreateReply:
  def run(message, user_claims, activity_uuid):
    model = {
      'errors': None,
      'data': None
    }

    if not user_claims:
      model['errors'] = ['user_not_authenticated']
      return model

    if activity_uuid == None or len(activity_uuid) < 1:
      model['errors'] = ['activity_uuid_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 1024:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      return model

    try:
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cognito_user_id = user_claims.get('sub')
          cur.execute("SELECT uuid, handle FROM public.users WHERE cognito_user_id = %s", (cognito_user_id,))
          user_result = cur.fetchone()
          
          if not user_result:
            model['errors'] = ['user_not_found']
            return model
          
          user_uuid, user_handle = user_result
          now = datetime.now(timezone.utc).astimezone()
          reply_uuid = uuid.uuid4()
          
          cur.execute("""
            INSERT INTO public.activities (uuid, user_uuid, message, reply_to_activity_uuid, created_at)
            VALUES (%s, %s, %s, %s, %s)
          """, (reply_uuid, user_uuid, message, activity_uuid, now))
          
          conn.commit()
          
    except Exception as e:
      model['errors'] = ['database_error']
      return model

    model['data'] = {
      'uuid': str(reply_uuid),
      'handle': user_handle,
      'message': message,
      'created_at': now.isoformat(),
      'reply_to_activity_uuid': activity_uuid
    }
    return model
