#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: MIT-0
 
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this
#  software and associated documentation files (the "Software"), to deal in the Software
#  without restriction, including without limitation the rights to use, copy, modify,
#  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so.
 
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import urllib.parse
import boto3
import base64
import os
import logging

# Environment Variables
LFV_PROJECT_NAME = os.environ['LFV_PROJECT_NAME']
LFV_MODEL_VERSION = os.environ['LFV_MODEL_VERSION']
REGION = os.environ.get('REGION', 'eu-west-1')
# Initiate clients
lookoutvision = boto3.client('lookoutvision')
s3 = boto3.client('s3')

print('Loading function')


def lambda_handler(event, context):
    bucket = event['Input']['Bucket']
    key = event['Input']['Key']
    try:
        response = detect_anomalies(bucket, key)
        return response
    except Exception as e:
        print(e)
        raise e


def detect_anomalies(bucket, key):

    try:
        response = s3.get_object(Bucket=bucket, Key=key)

        project_name = LFV_PROJECT_NAME
        model_version = LFV_MODEL_VERSION
        content_type = response['ContentType']
        image = response['Body']
        image_body = image.read()

        camera_id = response['Metadata']['cameraid']
        assembly_line_id = response['Metadata']['assemblylineid']
        image_id = response['Metadata']['imageid']

        lookout_response = lookoutvision.detect_anomalies(
            ProjectName=project_name,
            ModelVersion=model_version,
            Body=image_body,
            ContentType=content_type
        )

        lookout_response['CameraId'] = camera_id
        lookout_response['AssemblyLineId'] = assembly_line_id
        lookout_response['ImageId'] = image_id
        lookout_response['ImageUrl'] = 's3://'+bucket+'/'+key

        print(json.dumps(lookout_response))

        return lookout_response

    except Exception as e:

        print(e)
        raise e
