import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
apigateway = boto3.client('apigatewaymanagementapi',
    endpoint_url=os.environ.get('WEBSOCKET_API_ENDPOINT'))

def lambda_handler(event, context):
    connections_table = dynamodb.Table(os.environ['CONNECTIONS_TABLE'])
    
    for record in event['Records']:
        if record['eventName'] == 'INSERT' and record['dynamodb']['Keys']['pk']['S'].startswith('CONV#'):
            # New message inserted
            message_data = record['dynamodb']['NewImage']
            
            # Grab every active connection (small table so scan is fine)
            response = connections_table.scan()
            connections = response.get('Items', [])
            
            # Prepare message payload
            payload = {
                'type': 'new_message',
                'data': {
                    'conversation_id': record['dynamodb']['Keys']['pk']['S'].replace('CONV#', ''),
                    'message': message_data.get('message', {}).get('S', ''),
                    'sender_handle': message_data.get('sender_handle', {}).get('S', ''),
                    'timestamp': record['dynamodb']['Keys']['sk']['S']
                }
            }
            
            # Fan out to every active connection
            for connection in connections:
                try:
                    apigateway.post_to_connection(
                        ConnectionId=connection['connectionId'],
                        Data=json.dumps(payload)
                    )
                except Exception as e:
                    print(f"Failed to send to {connection['connectionId']}: {e}")
                    # Remove stale connection
                    connections_table.delete_item(
                        Key={'connectionId': connection['connectionId']}
                    )
    
    return {"statusCode": 200}
