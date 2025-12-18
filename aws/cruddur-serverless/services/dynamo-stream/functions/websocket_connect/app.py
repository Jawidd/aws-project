import os
from datetime import datetime, timedelta

import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    request_context = event.get('requestContext', {})
    connection_id = request_context.get('connectionId')

    if not connection_id:
        return {'statusCode': 400}

    table = dynamodb.Table(os.environ['CONNECTIONS_TABLE'])

    now = datetime.now()

    # Keep the connection for a day; stale ones fall out automatically
    ttl = int((now + timedelta(hours=24)).timestamp())

    table.put_item(
        Item={
            'connectionId': connection_id,
            'ttl': ttl,
            'connected_at': now.isoformat()
        }
    )

    return {'statusCode': 200}
