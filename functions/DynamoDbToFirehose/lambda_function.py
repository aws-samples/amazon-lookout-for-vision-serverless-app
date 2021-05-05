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

import os, json, base64, boto3, datetime

firehose = boto3.client('firehose')

print('Loading function')

def put_record_in_firehose(stream_record):
    new_image_item = stream_record['NewImage']
    transformed_item = {}
    # Transform the record a bit
    try:
        date_time_str = new_image_item['DateTime']['S']
        print(date_time_str)
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f')

        transformed_item['AssemblyLineId'] = new_image_item['AssemblyLineId']['S']
        transformed_item['CameraId'] = new_image_item['CameraId']['S']
        transformed_item['ImageId'] = new_image_item['ImageId']['S']
        transformed_item['ImageUrl'] = new_image_item['ImageUrl']['S']
        transformed_item['DateTime'] = new_image_item['DateTime']['S']
        transformed_item['IsAnomalous'] = new_image_item['IsAnomalous']['BOOL']
        transformed_item['Confidence'] = new_image_item['Confidence']['N']
        transformed_item['Year'] = date_time_obj.year
        transformed_item['Month'] = date_time_obj.month
        transformed_item['Day'] = date_time_obj.day
        transformed_item['Hour'] = date_time_obj.hour
        transformed_item['Minute'] = date_time_obj.minute
        transformed_item['Region'] = stream_record['awsRegion']
    except Exception as e:
        print(e)
    
    j_to_firehose = json.dumps(transformed_item)
    response = firehose.put_record(
    DeliveryStreamName=os.environ['DeliveryStreamName'],
    Record= {
                'Data': j_to_firehose + '\n'
            }
        )
    print(response)

def lambda_handler(event, context):
    for record in event['Records']:
        if (record['eventName']) == 'INSERT':
            put_record_in_firehose(record['dynamodb'])
    return 'Successfully processed {} records.'.format(len(event['Records']))

