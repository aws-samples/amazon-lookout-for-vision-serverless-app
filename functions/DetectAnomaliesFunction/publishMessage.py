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

import os
import boto3
import json
import logging
from decimal import Decimal

client = boto3.client('sns')
TARGET_ARN = os.environ['TARGET_ARN']
REGION = os.environ['REGION']
CONFIDENCE_THRESHOLD =  Decimal(os.environ['CONFIDENCE_THRESHOLD'])

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Publishes a message to a topic. 
    :return: The ID of the message.
    """

    try:
        payload = event['Input']['Payload']
        image_details = payload['ImageDetails']
        print(image_details)
        MESSAGE_ANOMALOUS_LOW_CONFIDENCE = 'Defect detected with LOW confidence for image with id: ' + image_details['ImageId'] + '\nImage URL: ' + image_details['ImageUrl'] + '\nDateTime:' + str(image_details['DateTime']) + '\nConfidence: ' + str(image_details['Confidence'])
        MESSAGE_ANOMALOUS = 'Defect detected for image with id: ' + image_details['ImageId'] + '\nImage URL: ' + image_details['ImageUrl'] + '\nDateTime:' + str(image_details['DateTime']) + '\nConfidence: ' + str(image_details['Confidence'])
        MESSAGE_NORMAL_LOW_CONFIDENCE = 'Low Confidence for non-anomalous image - \nImageId:' + image_details['ImageId'] + '\nImage URL: ' + image_details['ImageUrl'] + '\nDateTime:' + str(image_details['DateTime']) + '\nConfidence: ' + str(image_details['Confidence'])
        SUBJECT = 'Defect Detection Alert - ' + 'AssemblyLine: ' + image_details['AssemblyLineId'] + ' Camera: ' + image_details['CameraId']
        message = {"Body": "Defect detected for image " + image_details['ImageUrl']}
        confidence = Decimal(image_details['Confidence'])
        message_id = ''
        
        if(image_details['IsAnomalous']):
            print('Image is an anomaly - sending alert message')
            if(confidence < CONFIDENCE_THRESHOLD):
                response = client.publish(
                    TargetArn=TARGET_ARN,
                    Message=json.dumps({'default': json.dumps(message),
                                        'email': MESSAGE_ANOMALOUS_LOW_CONFIDENCE
                                        }),
                    Subject='LOW Confidence - ' + SUBJECT,
                    MessageStructure='json'
                )
            else:
                response = client.publish(
                    TargetArn=TARGET_ARN,
                    Message=json.dumps({'default': json.dumps(message),
                                        'email': MESSAGE_ANOMALOUS
                                        }),
                    Subject=SUBJECT,
                    MessageStructure='json'
                )
            message_id = response['MessageId']
            logger.info(
                "Published defect detected message to topic %s.", TARGET_ARN)
        else:
            
            if(confidence < CONFIDENCE_THRESHOLD):

                message = {"Body": "Defect detected for image " + image_details['ImageUrl']}
                response = client.publish(
                    TargetArn=TARGET_ARN,
                    Message=json.dumps({'default': json.dumps(message),
                                        'email': MESSAGE_NORMAL_LOW_CONFIDENCE
                                        }),
                    Subject='Low Confidence Alert for Non-anomalous image - ' + 'AssemblyLine: ' + image_details['AssemblyLineId'] + ' Camera: ' + image_details['CameraId'],
                    MessageStructure='json'
                )
                message_id = response['MessageId']
                logger.info("Published defect detected message to topic %s.", TARGET_ARN)

        return message_id
    except Exception as e:
        logger.exception("Couldn't publish message to topic %s.", TARGET_ARN)
        print(e)
        raise e
