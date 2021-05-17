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

from crhelper import CfnResource
import boto3, json


helper = CfnResource()
client = boto3.client('s3')

@helper.create
@helper.update
def create_s3_notification(event, context):
    lambda_arn=event['ResourceProperties']['LambdaArn']
    bucket=event['ResourceProperties']['Bucket']
    suffix=event['ResourceProperties']['Suffix']
    
    try:
        print("Request Type:",event['RequestType'])
        response = add_notification(lambda_arn, bucket, suffix)
        print(response)
    except Exception as e:
        print(e)
        raise e

@helper.delete
def delete_s3_notification(event, context):
    bucket = event['ResourceProperties']['Bucket']
    
    try:
        print("Request Type:",event['RequestType'])      
        delete_notification(bucket)
    except Exception as e:
        print(e)
        raise e


def handler(event, context):
    helper(event, context)
    
def add_notification(lambda_arn, bucket, suffix):
    response = client.put_bucket_notification_configuration(
        Bucket = bucket,
        NotificationConfiguration={
        'LambdaFunctionConfigurations': [
            {
                'Id':'Image-Uploded-Event',
                'LambdaFunctionArn': lambda_arn,
                'Events': [
                    's3:ObjectCreated:*'
                ],
                'Filter': {
                    'Key': {
                        'FilterRules': [
                            {
                                'Name': 'suffix',
                                'Value': suffix
                            }
                        ]
                    }
                }
            }
        ]
        }
    )
    
    print("Put request completed....")
    return response
def delete_notification(bucket):
    print("Delete request - No action required")
