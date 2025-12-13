from lib.db import db

class TrendingActivities:
  def run():
    sql = """
    SELECT 
      activities.uuid,
      activities.message,
      activities.likes_count,
      users.handle,
      users.full_name
    FROM public.activities
    LEFT JOIN public.users ON users.uuid = activities.user_uuid
    WHERE activities.likes_count > 0
    ORDER BY activities.likes_count DESC, activities.created_at DESC
    LIMIT 5
    """
    
    with db.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql)
        results = cur.fetchall()
        
        activities = []
        for result in results:
          activities.append({
            'uuid': str(result[0]),
            'message': result[1][:100] + '...' if len(result[1]) > 100 else result[1],
            'likes_count': result[2],
            'handle': result[3],
            'display_name': result[4] or result[3]
          })
        
        return activities