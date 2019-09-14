import json
import logging
import os
import sys
import time
import uuid
import jsonschema
from datetime import datetime
import boto3

from schema import Schema, And, Use, Optional

dynamodb = boto3.resource('dynamodb')


def create(event, context):
    schema = Schema(
        {
            'message': And(str, len)
        }
    )

    data = json.loads(event['body'])
    validated = schema.is_valid(data)

    if not validated:
        response = {
            "statusCode": 400,
            "body": {
                "error":  "Bad Request",
                "message": "Invalid request body"
            }
        }

    table = dynamodb.Table(os.environ['DYNAMODB_MESSAGES_TABLE'])

    timestamp = str(datetime.utcnow().timestamp())
    message = {
        'id': str(uuid.uuid1()),
        'message': data['message'],
        'createdAt': timestamp,
        'updatedAt': timestamp
    }

    table.put_item(Item=message)

    response = {
        "statusCode": 201,
        "body": json.dumps(message)
    }
    return response
