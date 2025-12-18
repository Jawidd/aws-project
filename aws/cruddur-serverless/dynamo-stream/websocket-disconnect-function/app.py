import os

import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    request_context = event.get('requestContext', {})
    connection_id = request_context.get('connectionId')

    if not connection_id:
        return {'statusCode': 400}

    table = dynamodb.Table(os.environ['CONNECTIONS_TABLE'])

    # Drop the connection record; clients will reconnect as needed
    table.delete_item(
        Key={'connectionId': connection_id}
    )

    return {'statusCode': 200}
