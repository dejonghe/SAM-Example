from __future__ import print_function

print('Loading function')

import boto3
import requests
import json
import sys
import os


print('Loading function')

session = boto3.session.Session(region_name=os.environ['region'])
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

        # Check if img query exists return 400 if not
        if img_url == '':
            err_resp = { 'usage': 'cats.codingforthecloud.com/?img=<HTTP Link> img must be png or jpg. JSON returned, { "cats": BOOL, "confidence": "0.0%" }.' }
            return respond(res=err_resp, status=400)
 
        # Check if img extention is jpg or png return 415 if not (naive but good enough for who it's for)
        if img_format != 'jpg' and img_format != 'png':
            err_resp = { 'error': 'Must be png or jpg'}
            return respond(res=err_resp, status=415)

        # Download the image
        image = requests.get(img_url).content

        # Check the image size to ensure it's less than 5MB return 413 if it's larger
        img_size = sys.getsizeof(image)
        if img_size > 5000000:
            err_resp = { 'error': "Size must be less than 5MB your size is {0} Bytes.".format(str(img_size)) }
            return respond(res=err_resp, status=413)

        # Send image to rekognition service
        kog = rek.detect_labels(
            Image={
                'Bytes':image
            }
        )
       
        # Look for cats label 
        for label in kog['Labels']:
            if label['Name'] == 'Cat':
                resp = { 'cats': { 'isACat': True, "confidence": label['Confidence'] } }
        if 'resp' not in vars():
            resp = { 'cats': { 'isACat': False, "confidence": 98 } }

        kog = rek.recognize_celebrities(
            Image={
                'Bytes':image
            }
        )
        for celeb in kog['CelebrityFaces']:
            resp.setdefault('celebs', []).append({ 'celeb': celeb['Name'], 'confidence': celeb['MatchConfidence']}) 
        
        # Return to client
        return respond(res=resp)
    else:
        # Return 405 if client used any method but GET
        return respond(status=405, res={"error":"Method Not Allowed"})

if __name__ == "__main__":
  lambda_handler()
