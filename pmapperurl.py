import boto3
from boto3 import client as boto3_client
import s3util
import json
import os
from datetime import datetime

lambda_client = boto3_client('lambda')

BUCKET_NAME = ''
BUCKET_REGION = ''


LOCAL_STORAGE_PATH = "/tmp/"

def lambda_handler(event, context):
    
    BUCKET_NAME = event['queryStringParameters']['bucketname']
    BUCKET_REGION = event['queryStringParameters']['bucketregion']
    
    
    dateNow = datetime.now()
    unique_outputFile = "output_" + dateNow.strftime("%H-%M-%S-%f")
    s3ObjectName = unique_outputFile + '.svg'
    
    signedURL = create_signed_URL(BUCKET_NAME, s3ObjectName, BUCKET_REGION) 
    print(signedURL)
    print('&&&&&&&&&&&&&-------------&&&&&&&&&&&&&&&&')
    
    payload = {}
    payload['bucketname'] = BUCKET_NAME
    payload['bucketregion'] = BUCKET_REGION
    
    lambda_client.invoke(
    FunctionName='arn:aws:lambda:eu-west-1:206322004324:function:pmapper-s3-12092020',
    InvocationType='Event',
    Payload=json.dumps(payload)
    )
    
    apiResponse = {}
    apiResponse['signedURL'] = signedURL
    apiResponse['message'] = "Please click on the URL to get access to the output file"
   
    
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['isBase64Encoded'] = False
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(apiResponse)
    return responseObject

    

def create_signed_URL(BUCKET_NAME,outputObjectName,BUCKET_REGION):
    signedURL = s3util.create_presigned_url(BUCKET_NAME, outputObjectName, BUCKET_REGION)
    return signedURL
    
    
if __name__ == '__main__':
    lambda_handler(None, None) 