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
    def run(message: str, sender_user: dict, receiver_user: dict, endpoint_url=None):
        model = {"errors": None, "data": None}

        if not message:
            model["errors"] = ["message_blank"]
            return model

        try:
            conv_table = CreateMessage.get_conversations_table(endpoint_url)
            msg_table = CreateMessage.get_messages_table(endpoint_url)

            user_sender_uuid = sender_user["uuid"]
            user_receiver_uuid = receiver_user["uuid"]

            response = conv_table.query(
                KeyConditionExpression=Key("pk").eq(f"USER#{user_sender_uuid}")
            )

            conv_item = next(
                (item for item in response.get("Items", []) if item.get("other_handle") == user_receiver_uuid),
                None
            )

            now = datetime.now(timezone.utc).isoformat()

            if conv_item:
                conv_id = conv_item["sk"].replace("CONV#", "")
                # Update last message in existing conversation
                conv_table.update_item(
                    Key={"pk": f"USER#{user_sender_uuid}", "sk": f"CONV#{conv_id}"},
                    UpdateExpression="SET last_message_text = :msg, last_message_timestamp = :ts",
                    ExpressionAttributeValues={":msg": message, ":ts": now}
                )
                conv_table.update_item(
                    Key={"pk": f"USER#{user_receiver_uuid}", "sk": f"CONV#{conv_id}"},
                    UpdateExpression="SET last_message_text = :msg, last_message_timestamp = :ts",
                    ExpressionAttributeValues={":msg": message, ":ts": now}
                )
            else:
                conv_id = str(uuid.uuid4())

                conv_table.put_item(Item={
                    "pk": f"USER#{user_sender_uuid}",
                    "sk": f"CONV#{conv_id}",
                    "last_message_text": message,
                    "last_message_timestamp": now,
                    "participants": [user_sender_uuid, user_receiver_uuid],
                    "other_handle": receiver_user["handle"],
                    "other_display_name": receiver_user.get("preferred_username") or receiver_user.get("full_name") or receiver_user["handle"],
                    "other_full_name": receiver_user.get("full_name") or receiver_user.get("preferred_username") or receiver_user["handle"]
                })

                conv_table.put_item(Item={
                    "pk": f"USER#{user_receiver_uuid}",
                    "sk": f"CONV#{conv_id}",
                    "last_message_text": message,
                    "last_message_timestamp": now,
                    "participants": [user_sender_uuid, user_receiver_uuid],
                    "other_handle": sender_user["handle"],
                    "other_display_name": sender_user.get("preferred_username") or sender_user.get("full_name") or sender_user["handle"],
                    "other_full_name": sender_user.get("full_name") or sender_user.get("preferred_username") or sender_user["handle"]
                })

            msg_uuid = str(uuid.uuid4())
            sk = f"MSG#{now}#{msg_uuid}"

            msg_table.put_item(Item={
                "pk": f"CONV#{conv_id}",
                "sk": sk,
                "message": message,
                "sender_uuid": user_sender_uuid,
                "sender_handle": sender_user["handle"],
                "sender_full_name": sender_user.get("full_name") or sender_user.get("preferred_username") or sender_user["handle"],
                "recipient_uuids": [user_receiver_uuid]
            })

            model["data"] = {
                "uuid": msg_uuid,
                "display_name": sender_user.get("full_name") or sender_user.get("preferred_username") or sender_user["handle"],
                "handle": sender_user["handle"],
                "full_name": sender_user.get("full_name") or sender_user.get("preferred_username") or sender_user["handle"],
                "message": message,
                "created_at": now
            }

        except Exception as e:
            current_app.logger.error(f"Error in CreateMessage.run: {e}", exc_info=True)
            model["errors"] = [str(e)]

        return model
