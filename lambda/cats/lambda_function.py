from __future__ import print_function

print('Loading function')

import boto3
import requests
import json
import sys


print('Loading function')

session = boto3.session.Session(region_name='us-east-1')
rek = session.client('rekognition')

def respond(status=200, res=None):
    return {
        'statusCode': str(status),
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    print("Received event: " + json.dumps(event, indent=2))

    operations = [
        'GET'
    ]

    operation = event['requestContext']['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters']
        img_url = payload['img']
        img_format = img_url.split('.')[-1]
        if img_url == '':
            resp = { 'usage': 'isporn.codingforthecloud.com/?img=<HTTP Link> img must be png or jpg. JSON returned, { "porn": BOOL, "detail": "detail if is porn" }.' }
            return respond(res=resp, status=400)
        if img_format != 'jpg' and img_format != 'png':
            resp = { 'error': 'Must be png or jpg'}
            return respond(res=resp, status=415)
        image = requests.get(img_url).content
        img_size = sys.getsizeof(image)
        if img_size > 5000000:
            resp = { 'error': "Size must be less than 5MB your size is {0} Bytes.".format(str(img_size)) }
            return respond(res=resp, status=413)
        kog = rek.detect_moderation_labels(
            Image={
                'Bytes':image
            }
        )
        iteration = 0
        if kog['ModerationLabels']:
            for label in kog['ModerationLabels']:
                if label['ParentName'] == 'Explicit Nudity':
                    explicit = iteration
                if label['ParentName'] == 'Suggestive':
                    suggestive = iteration
                iteration += 1
        else:
            resp = { 'porn': False, 'detail': None }
        if 'explicit' in vars():
            resp = { 'porn': True, 'detail': kog['ModerationLabels'][explicit]['Name'] }
        elif 'suggestive' in vars():
            resp = { 'porn': True, 'detail': kog['ModerationLabels'][suggestive]['Name'] }
        return respond(res=resp)

        return respond(None, operations[operation](dynamo, payload))
    else:
        return respond(status=405, res={"error":"Method Not Allowed"})

if __name__ == "__main__":
  lambda_handler()
