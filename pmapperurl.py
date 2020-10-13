import boto3
from boto3 import client as boto3_client
import s3util
import json
import os
from datetime import datetime
import urllib3 
from botocore.vendored import requests


lambda_client = boto3_client('lambda')

BUCKET_NAME = ''
BUCKET_REGION = ''


LOCAL_STORAGE_PATH = "/tmp/"

def lambda_handler(event, context):
    
    BUCKET_NAME = event['queryStringParameters']['bucketname']
    BUCKET_REGION = event['queryStringParameters']['bucketregion']
    
    dateNow = datetime.now()
    unique_outputFile = "output_" + dateNow.strftime("%H-%M-%S-%f")
    unique_outputFile2 = "report_" + dateNow.strftime("%H-%M-%S-%f")
    s3ObjectName = unique_outputFile + '.svg'
    s3ObjectName2 = unique_outputFile2 + '.json'
    
    payload = {"bucketname": BUCKET_NAME, "bucketregion": BUCKET_REGION, "s3objectname": s3ObjectName, "s3objectname2": s3ObjectName2}
    
    url = 'https://gm9z2qdgxf.execute-api.eu-west-2.amazonaws.com/dev/pmapper-s3'
    requests.post(url, data = json.dumps(payload))

    signedURL = create_signed_URL(BUCKET_NAME, s3ObjectName, BUCKET_REGION) 
    signedURL2 = create_signed_URL(BUCKET_NAME, s3ObjectName2, BUCKET_REGION)

    apiResponse = {}
    apiResponse['signedURL'] = signedURL 
    apiResponse['signedURL2'] = signedURL2
    apiResponse['message'] = "Thank you for your request. You can use the link above to download your report. Please allow up to 10 mins"
   
    
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['isBase64Encoded'] = False
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(apiResponse)
    return responseObject
    

def create_signed_URL(BUCKET_NAME,outputObjectName,BUCKET_REGION):
    signedURL = s3util.create_presigned_url(BUCKET_NAME, outputObjectName, BUCKET_REGION)
    signedURL2 = s3util.create_presigned_url(BUCKET_NAME, outputObjectName, BUCKET_REGION)
    return {signedURL:'signedURL', signedURL2:'signedURL2'}
    
    
if __name__ == '__main__':
    lambda_handler(None, None) 
