from datetime import datetime, timedelta, timezone

# import XRay SDK libraries
from aws_xray_sdk.core import xray_recorder

class NotificationsActivities:
  def __init__(self, request):
        self.request = request
        
  def run(self,user_handle):
    try:
      # Start a segment
      parent_subsegment = xray_recorder.begin_subsegment('notifications_activities_start')
      parent_subsegment.put_annotation('url', self.request.url)
      model = {
        'errors': None,
        'data': None
      }
      
      if user_handle == None or len(user_handle) < 1:
        model['errors'] = ['blank_user_handle']
      else:
        try:
          # Start a subsegment
          subsegment = xray_recorder.begin_subsegment('notif_activiteis_nested_subsegment')
          
          now = datetime.now(timezone.utc).astimezone()
          results = [{
            'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
            'handle':  'James Kirk',
            'message': 'To boldly go where no one has gone before!',
            'created_at': (now - timedelta(days=2)).isoformat(),
            'expires_at': (now + timedelta(days=5)).isoformat(),
            'likes_count': 5,
            'replies_count': 1,
            'reposts_count': 0,
            'replies': [{
              'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
              'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
              'handle':  'Worf',
              'message': 'This post has no honor!',
              'likes_count': 0,
              'replies_count': 0,
              'reposts_count': 0,
              'created_at': (now - timedelta(days=2)).isoformat()
            }],
          }]# return results
          
          model['data'] = results
          # subsegment.put_annotation('user_handle', results)
        except Exception as e:
          # Raise the error in the segment
          raise e
        finally:  
          xray_recorder.end_subsegment()
    except Exception as e:
      # Raise the error in the segment
      raise e
    finally:  
      # Close the segment
      xray_recorder.end_subsegment()
    return model
          
          