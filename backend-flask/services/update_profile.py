from lib.db import db
import logging

class UpdateProfile:
  def run(cognito_user_id,bio,display_name):
    logging.info(f"UpdateProfile.run: cognito_user_id={cognito_user_id}, bio='{bio}', display_name='{display_name}'")
    
    if display_name == None or len(display_name) < 1:
      logging.error("Display name is blank")
      return {'errors': ['display_name_blank'], 'data': None}
    
    try:
      sql = """
        UPDATE public.users 
        SET bio = %(bio)s, full_name = %(display_name)s
        WHERE cognito_user_id = %(cognito_user_id)s
        RETURNING handle, uuid, full_name, bio, created_at, avatar_url
      """
      
      params = {
        'bio': bio or '',
        'display_name': display_name,
        'cognito_user_id': cognito_user_id
      }
      
      logging.info(f"Executing SQL: {sql}")
      logging.info(f"With params: {params}")
      
      with db.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql, params)
          result = cur.fetchone()
          conn.commit()
          
          logging.info(f"SQL result: {result}")
          
          if result:
            data = {
              'handle': result[0],
              'uuid': str(result[1]),
              'display_name': result[2],
              'bio': result[3],
              'created_at': str(result[4]),
              'avatar_url': result[5]
            }
            logging.info(f"Returning data: {data}")
            return {
              'errors': None,
              'data': data
            }
          else:
            logging.error("No user found with the given cognito_user_id")
            return {'errors': ['User not found'], 'data': None}
        
    except Exception as e:
      logging.error(f"Exception in UpdateProfile: {str(e)}")
      return {'errors': [str(e)], 'data': None}
