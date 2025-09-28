import os
from datetime import datetime, timezone
import boto3
from flask import current_app
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

USER_PREFIX = "USER#"
CONV_PREFIX = "CONV#"

class MessageGroups:
    @staticmethod
    def get_table(endpoint_url=None):
        table_name = os.getenv("DYNAMODB_CONVERSATIONS_TABLE", "conversations")
        return boto3.resource(
            "dynamodb",
            region_name="eu-west-2",
            endpoint_url=endpoint_url
        ).Table(table_name)

    @staticmethod
    def run(user_uuid,user_full_name ,endpoint_url=None):
        table = MessageGroups.get_table(endpoint_url)
        pk_value = f"{USER_PREFIX}{user_uuid}"

        # Try GSI first, fallback to base table
        try:
            response = table.query(
                IndexName="LastMessageIndex",
                KeyConditionExpression=Key("pk").eq(pk_value),
                ScanIndexForward=False
            )
        except ClientError as e:
            current_app.logger.warning(f"GSI query failed ({e}), falling back to base query")
            response = table.query(KeyConditionExpression=Key("pk").eq(pk_value))

        items = sorted(
            response.get("Items", []),
            key=lambda x: x.get("last_message_timestamp", ""),
            reverse=True
        )
        def build_group(item):
            return {
                "uuid": item["sk"].replace(CONV_PREFIX, ""),
                "original_uuid": item.get("other_handle", "Unknown"),
                "full_name": item.get("other_full_name", "Unknown"),
                "handle": item.get("other_display_name", "unknown"),
                "message": item.get("last_message_text", ""),
                "created_at": item.get("last_message_timestamp", datetime.now(timezone.utc).isoformat())
            }

        groups = [build_group(i) for i in items]
        return {"data": groups, "errors": None}
