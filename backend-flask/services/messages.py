import os
from flask import current_app
import boto3
from boto3.dynamodb.conditions import Key
from services import users  # move import to top unless circular import

USER_PREFIX = "USER#"
CONV_PREFIX = "CONV#"
MSG_PREFIX = "MSG#"

class Messages:

    @staticmethod
    def _get_table(env_var: str, default_name: str, endpoint_url=None):
        """Helper to get DynamoDB table."""
        table_name = os.getenv(env_var, default_name)
        return boto3.resource(
            "dynamodb",
            region_name="eu-west-2",
            endpoint_url=endpoint_url
        ).Table(table_name)

    @staticmethod
    def get_conversations_table(endpoint_url=None):
        return Messages._get_table("DYNAMODB_CONVERSATIONS_TABLE", "conversations", endpoint_url)

    @staticmethod
    def get_messages_table(endpoint_url=None):
        return Messages._get_table("DYNAMODB_MESSAGES_TABLE", "messages", endpoint_url)

    @staticmethod
    def run(user_sender_cognito_id, user_receiver_uuid, endpoint_url=None):
        model = {"data": [], "errors": None}
        try:
            current_app.logger.info(f"Messages.run started for sender={user_sender_cognito_id} receiver={user_receiver_uuid}")

            # 1️⃣ Convert sender Cognito ID to UUID
            sender = users.UsersService.get_user_by_cognito_id(user_sender_cognito_id)
            if not sender:
                model['errors'] = f"Sender {user_sender_cognito_id} not found"
                return model
            sender_uuid = sender['uuid']

            # 2️⃣ Tables
            conv_table = Messages.get_conversations_table(endpoint_url)
            msg_table = Messages.get_messages_table(endpoint_url)

            # 3️⃣ Find the conversation
            response = conv_table.query(KeyConditionExpression=Key('pk').eq(f"{USER_PREFIX}{sender_uuid}"))
            conv_item = next(
                (item for item in response.get('Items', [])
                 if item.get('other_handle') == user_receiver_uuid),
                None
            )

            if not conv_item:
                current_app.logger.info(f"No conversation found between {sender_uuid} and {user_receiver_uuid}")
                return model  # empty list

            conv_id = conv_item['sk'].replace(CONV_PREFIX, '')

            # 4️⃣ Fetch messages
            pk_value = f"{CONV_PREFIX}{conv_id}"
            response = msg_table.query(KeyConditionExpression=Key('pk').eq(pk_value), ScanIndexForward=True)
            current_app.logger.info(f" 001messages for conversation {response}")
            messages_list = [
                {
                    "uuid": sk.split('#')[2],
                    "display_name": sender_uuid if item['sender_handle'] == sender_uuid else user_receiver_uuid,
                    "handle": item['sender_handle'],
                    "message": item['message'],
                    "full_name": item.get('sender_full_name', item.get('sender_handle', 'Unknown')), 
                    "created_at": sk.split('#')[1]
                }
                for item in response.get('Items', [])
                for sk in [item['sk']]  # unpack sk inside list comprehension
            ]

            model['data'] = messages_list
            current_app.logger.info(f"12Fetched {len(messages_list)} messages for conversation {conv_id}")

        except Exception as e:
            current_app.logger.error(f"Error in Messages.run: {e}", exc_info=True)
            model['errors'] = str(e)

        return model
