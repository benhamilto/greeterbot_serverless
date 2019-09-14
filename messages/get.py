import os
import json

import boto3
dynamodb = boto3.resource('dynamodb')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_MESSAGES_TABLE'])

    message = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(message['Item'])
    }

    return response
