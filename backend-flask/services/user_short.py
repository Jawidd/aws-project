from lib.db import db
import logging

class UserShort:
  def run(handle):
    logging.info(f"UserShort.run called with handle: {handle}")
    try:
      sql = """
      SELECT
        users.uuid,
        users.handle,
        users.full_name as display_name,
        users.bio,
        users.created_at
      FROM public.users
      WHERE 
        users.handle = %(handle)s
      """
      
      logging.info(f"Executing SQL: {sql} with handle: {handle}")
      results = db.query_object_json(sql,{
        'handle': handle
      })
      logging.info(f"UserShort query result: {results}")
      return results
    except Exception as e:
      logging.error(f"UserShort error: {str(e)}")
      # Convert URL-safe handle back to display format
      display_name = handle.replace('_at_', '@').replace('_', '.')
      
      # Fallback when database is not available
      fallback = {
        'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
        'handle': handle,
        'display_name': display_name,
        'bio': 'Welcome to Cruddur! This is your profile.',
        'created_at': '2023-01-01T00:00:00.000000+00:00'
      }
      logging.info(f"UserShort fallback: {fallback}")
      return fallback