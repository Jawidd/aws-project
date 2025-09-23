import json
import psycopg2
import os

def lambda_handler(event, context):
    try:
        # Extract user data from Cognito event
        user_attributes = event['request']['userAttributes']
        cognito_user_id = event['userName']
        email = user_attributes.get('email')
        preferred_username = user_attributes.get('preferred_username')
        handle = email.split('@')[0]
        
        # Connect to database
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cur = conn.cursor()
        
        # Insert user if not exists
        cur.execute("""
            INSERT INTO public.users (preferred_username, handle, email, cognito_user_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
            """, (preferred_username, handle, email, cognito_user_id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"User created: {email}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e
    
    return event
