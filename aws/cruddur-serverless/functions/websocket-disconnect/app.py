import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    table_name = os.environ['CONNECTIONS_TABLE']
    table = dynamodb.Table(table_name)
    
    # Remove connection
    table.delete_item(
        Key={'connectionId': connection_id}
    )
    
    return {'statusCode': 200}