import os
import json

import boto3
dynamodb = boto3.resource('dynamodb')


def list(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_MESSAGES_TABLE'])

    messages = table.scan()

    response = {
        "statusCode": 200,
        "body": json.dumps(messages['Items'])
    }

    return response
