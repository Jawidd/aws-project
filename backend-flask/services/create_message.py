import os
import uuid
from datetime import datetime, timezone
from flask import current_app
import boto3
from boto3.dynamodb.conditions import Key

class CreateMessage:

    @staticmethod
    def _get_table(env_var: str, default_name: str, endpoint_url=None):
        table_name = os.getenv(env_var, default_name)
        return boto3.resource(
            "dynamodb",
            region_name="eu-west-2",
            endpoint_url=endpoint_url
        ).Table(table_name)

    @staticmethod
    def get_conversations_table(endpoint_url=None):
        return CreateMessage._get_table("DYNAMODB_CONVERSATIONS_TABLE", "conversations", endpoint_url)

    @staticmethod
    def get_messages_table(endpoint_url=None):
        return CreateMessage._get_table("DYNAMODB_MESSAGES_TABLE", "messages", endpoint_url)

    @staticmethod
    def run(message: str, user_sender_uuid: str, user_receiver_uuid: str, endpoint_url=None):
        model = {"errors": None, "data": None}

        if not message:
            model["errors"] = ["message_blank"]
            return model

        try:
            conv_table = CreateMessage.get_conversations_table(endpoint_url)
            msg_table = CreateMessage.get_messages_table(endpoint_url)

            # Check if conversation exists
            response = conv_table.query(
                KeyConditionExpression=Key("pk").eq(f"USER#{user_sender_uuid}")
            )

            conv_item = next(
                (item for item in response.get("Items", []) if item.get("other_handle") == user_receiver_uuid),
                None
            )

            if conv_item:
                conv_id = conv_item["sk"].replace("CONV#", "")
            else:
                # Create new conversation
                conv_id = str(uuid.uuid4())
                now = datetime.now(timezone.utc).isoformat()
                
                conv_table.put_item(Item={
                    "pk": f"USER#{user_sender_uuid}",
                    "sk": f"CONV#{conv_id}",
                    "last_message_text": message,
                    "last_message_timestamp": now,
                    "participants": [user_sender_uuid, user_receiver_uuid],
                    "other_handle": user_receiver_uuid,
                    "other_display_name": user_receiver_uuid
                })
                
                conv_table.put_item(Item={
                    "pk": f"USER#{user_receiver_uuid}",
                    "sk": f"CONV#{conv_id}",
                    "last_message_text": message,
                    "last_message_timestamp": now,
                    "participants": [user_sender_uuid, user_receiver_uuid],
                    "other_handle": user_sender_uuid,
                    "other_display_name": user_sender_uuid
                })

            # Store the message
            now = datetime.now(timezone.utc).isoformat()
            msg_uuid = str(uuid.uuid4())
            sk = f"MSG#{now}#{msg_uuid}"
            
            msg_table.put_item(Item={
                "pk": f"CONV#{conv_id}",
                "sk": sk,
                "message": message,
                "sender_uuid": user_sender_uuid,
                "sender_handle": user_sender_uuid,
                "recipient_uuids": [user_receiver_uuid]
            })

            model["data"] = {
                "uuid": msg_uuid,
                "sender_uuid": user_sender_uuid,
                "message": message,
                "created_at": now
            }

        except Exception as e:
            current_app.logger.error(f"Error in CreateMessage.run: {e}", exc_info=True)
            model["errors"] = [str(e)]

        return model
