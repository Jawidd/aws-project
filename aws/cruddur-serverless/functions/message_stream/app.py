import json
import os

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

apigateway = boto3.client(
    'apigatewaymanagementapi',
    endpoint_url=os.environ.get('WEBSOCKET_API_ENDPOINT')
)


def lambda_handler(event, context):
    connections_table = dynamodb.Table(os.environ['CONNECTIONS_TABLE'])

    for record in event.get('Records', []):
        # Only react to new messages for conversations
        if record.get('eventName') != 'INSERT':
            continue

        keys = record.get('dynamodb', {}).get('Keys', {})
        pk = keys.get('pk', {}).get('S')

        if not pk or not pk.startswith('CONV#'):
            continue

        new_image = record.get('dynamodb', {}).get('NewImage', {})

        # Prepare message payload
        payload = {
            'type': 'new_message',
            'data': {
                'conversation_id': pk.replace('CONV#', ''),
                'message': new_image.get('message', {}).get('S', ''),
                'sender_handle': new_image.get('sender_handle', {}).get('S', ''),
                'timestamp': keys.get('sk', {}).get('S')
            }
        }

        # Grab every active connection (small table so scan is fine)
        connections = []
        scan_kwargs = {}

        while True:
            response = connections_table.scan(**scan_kwargs)
            connections.extend(response.get('Items', []))

            if 'LastEvaluatedKey' not in response:
                break

            scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']

        # Fan out to every active connection
        for connection in connections:
            connection_id = connection.get('connectionId')

            if not connection_id:
                continue

            try:
                apigateway.post_to_connection(
                    ConnectionId=connection_id,
                    Data=json.dumps(payload)
                )

            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code')

                # Connection is stale, remove it
                if error_code == 'GoneException':
                    print(f"Removing stale connection: {connection_id}")

                    connections_table.delete_item(
                        Key={'connectionId': connection_id}
                    )
                else:
                    print(f"Failed to send to {connection_id}: {e}")

    return {'statusCode': 200}
