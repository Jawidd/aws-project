from datetime import datetime, timedelta, timezone
# Import aws-X-Ray SDK
from aws_xray_sdk.core import xray_recorder

class NotificationsActivities:
  def run():
    # aws-xray create a segment for tracing
    segment = xray_recorder.begin_segment('notifs-activities-all-mock-data')
    
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
    }]
    # Add metadata and annotations to the segment for filtering in aws-X-Ray
    segment.put_annotation('method', 'notifis_run')
    segment.put_annotation('results_count', len(results))
 
    
    
    return results
  
   