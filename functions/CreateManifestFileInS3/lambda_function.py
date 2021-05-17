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
def create_manifest_file(event, context):
    bucket_name = event['ResourceProperties']['BucketName']
    prefix = event['ResourceProperties']['Prefix']
    manifest_file_name = event['ResourceProperties']['ManifestFileName']
    try:
        uri_prefixes = { "URIPrefixes" : [ prefix ] }
        global_upload_settings = {"format" : "JSON"}
        file_locations = [uri_prefixes]

        data_set = {
            "fileLocations" : file_locations,
            "globalUploadSettings" : global_upload_settings
        }

        json_dump = json.dumps(data_set)
        print(json_dump)
        response = client.put_object(
            Bucket = bucket_name,
            Key = manifest_file_name,
            Body = json_dump.encode('utf-8')
        )
        print(response)
    except Exception as e:
        print(e)
        raise e

@helper.delete
def delete_manifest_file(event, context):
    bucket_name = event['ResourceProperties']['BucketName']
    manifest_file_name = event['ResourceProperties']['ManifestFileName']
    try:
        response = client.delete_object(
            Bucket = bucket_name,
            Key = manifest_file_name
        )
        print(response)
    except Exception as e:
        print(e)
        raise e


@helper.update
def update_manifest_file(event, context):
    print('Update called - no action required')


def handler(event, context):
    helper(event, context)
