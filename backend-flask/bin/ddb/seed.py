#!/home/jawid/workspace/aws/aws-project/backend-flask/venv/bin/python

import os
from dotenv import load_dotenv
from pathlib import Path
import boto3
import uuid
from datetime import datetime, timedelta

# Load .env file from parent directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get DynamoDB attributes
attrs = {}
local_url = os.getenv("DYNAMODB_LOCAL_URL")
if local_url:
    attrs['endpoint_url'] = local_url

table_name = os.getenv("DYNAMODB_TABLE_NAME", "cruddur-messages")

# Create DynamoDB resource
ddb = boto3.resource('dynamodb', **attrs)
table = ddb.Table(table_name)

# Users data (match your previous seed)
users = {
    "jawid00786": {
        "uuid": "b1116ed1-cab0-4dcd-8e8a-817ef3ebbc6a",
        "handle": "jawid00786"
    },
    "alice123": {
        "uuid": "a2227ff2-dde1-4abc-9f1e-1234567890ab",
        "handle": "alice123"
    },
    "bob456": {
        "uuid": "d4449ff4-ffee-4def-8b2c-123456abcdef",
        "handle": "bob456"
    }
}

def seed_messages():
    """
    Seed messages between users into DynamoDB.
    Each conversation gets a unique message group UUID.
    """
    now = datetime.now()

    # Example conversation 1: jawid00786 <-> Alice
    group1_uuid = str(uuid.uuid4())
    messages_group1 = [
        {
            "pk": f"MSG#{group1_uuid}",
            "sk": (now - timedelta(minutes=10)).isoformat(),
            "message_uuid": str(uuid.uuid4()),
            "user_uuid": users["jawid00786"]["uuid"],
            "user_handle": users["jawid00786"]["handle"],
            "message": "Hey Alice! How's it going?"
        },
        {
            "pk": f"MSG#{group1_uuid}",
            "sk": (now - timedelta(minutes=8)).isoformat(),
            "message_uuid": str(uuid.uuid4()),
            "user_uuid": users["alice123"]["uuid"],
            "user_handle": users["alice123"]["handle"],
            "message": "Hi Jawid! All good, just working on the project."
        },
        {
            "pk": f"MSG#{group1_uuid}",
            "sk": (now - timedelta(minutes=5)).isoformat(),
            "message_uuid": str(uuid.uuid4()),
            "user_uuid": users["jawid00786"]["uuid"],
            "user_handle": users["jawid00786"]["handle"],
            "message": "Great! Let's review it later."
        }
    ]

    # Example conversation 2: Alice <-> Bob
    group2_uuid = str(uuid.uuid4())
    messages_group2 = [
        {
            "pk": f"MSG#{group2_uuid}",
            "sk": (now - timedelta(minutes=7)).isoformat(),
            "message_uuid": str(uuid.uuid4()),
            "user_uuid": users["alice123"]["uuid"],
            "user_handle": users["alice123"]["handle"],
            "message": "Hey Bob, welcome to the team!"
        },
        {
            "pk": f"MSG#{group2_uuid}",
            "sk": (now - timedelta(minutes=3)).isoformat(),
            "message_uuid": str(uuid.uuid4()),
            "user_uuid": users["bob456"]["uuid"],
            "user_handle": users["bob456"]["handle"],
            "message": "Thanks Alice! Excited to work with everyone."
        }
    ]

    # Batch write messages
    try:
        with table.batch_writer() as batch:
            for msg in messages_group1 + messages_group2:
                batch.put_item(Item=msg)
        print(f"Seeded messages for groups {group1_uuid} and {group2_uuid}")
    except Exception as e:
        print("Error seeding messages:", e)

if __name__ == "__main__":
    seed_messages()
