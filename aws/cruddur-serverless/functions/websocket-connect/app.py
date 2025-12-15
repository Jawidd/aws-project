import json
import os
from datetime import datetime, timedelta

import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    table_name = os.environ['CONNECTIONS_TABLE']
    table = dynamodb.Table(table_name)
    
    # Keep the connection for a day; stale ones fall out automatically
    ttl = int((datetime.now() + timedelta(hours=24)).timestamp())
    
    table.put_item(
        Item={
            'connectionId': connection_id,
            'ttl': ttl,
            'connected_at': datetime.now().isoformat()
        }
    )
    
    return {'statusCode': 200}
