import json
import boto3

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] in ['INSERT', 'MODIFY', 'REMOVE']:
            print(f"Processing {record['eventName']} event")
            # Add your stream processing logic here
    
    return {"statusCode": 200}
