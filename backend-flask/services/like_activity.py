from lib.db import db
import logging

class LikeActivity:
    @staticmethod
    @staticmethod
    def run(activity_uuid, user_claims):
        if not user_claims:
            return {'errors': ['Authentication required']}
            
        try:
            with db.pool.connection() as conn:
                with conn.cursor() as cur:
                    # Get user UUID from cognito_user_id
                    cur.execute("""
                        SELECT uuid FROM public.users 
                        WHERE cognito_user_id = %s
                    """, (user_claims['sub'],))
                    
                    user_result = cur.fetchone()
                    if not user_result:
                        return {'errors': ['User not found']}
                    
                    user_uuid = user_result[0]
                    
                    # Check if activity exists and get current likes
                    cur.execute("""
                        SELECT uuid, likes_count 
                        FROM public.activities 
                        WHERE uuid = %s
                    """, (activity_uuid,))
                    
                    activity = cur.fetchone()
                    if not activity:
                        return {'errors': ['Activity not found']}
                    
                    current_likes = activity[1] or 0
                    
                    # Check if user already liked this activity
                    cur.execute("""
                        SELECT COUNT(*) FROM public.likes 
                        WHERE user_uuid = %s AND activity_uuid = %s
                    """, (user_uuid, activity_uuid))
                    
                    already_liked = cur.fetchone()[0] > 0
                    
                    if already_liked:
                        # Unlike: remove like and decrement count
                        cur.execute("""
                            DELETE FROM public.likes 
                            WHERE user_uuid = %s AND activity_uuid = %s
                        """, (user_uuid, activity_uuid))
                        
                        new_likes_count = max(0, current_likes - 1)
                        liked = False
                    else:
                        # Like: add like and increment count
                        cur.execute("""
                            INSERT INTO public.likes (user_uuid, activity_uuid, created_at) 
                            VALUES (%s, %s, CURRENT_TIMESTAMP)
                        """, (user_uuid, activity_uuid))
                        
                        new_likes_count = current_likes + 1
                        liked = True
                    
                    # Update activity likes count
                    cur.execute("""
                        UPDATE public.activities 
                        SET likes_count = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE uuid = %s
                        RETURNING likes_count
                    """, (new_likes_count, activity_uuid))
                    
                    updated_count = cur.fetchone()[0]
                    conn.commit()
                    
                    return {
                        'activity_uuid': activity_uuid,
                        'likes_count': updated_count,
                        'liked': liked
                    }
                    
        except Exception as e:
            logging.error(f"Error in LikeActivity.run: {str(e)}")
            return {'errors': [str(e)]}