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
 
#!/usr/bin/python

import os
import sys
import datetime
import time
sys.path.extend(["packages","scripts/packages"])
import requests

# Execute as - script.py SourceDirectoryPath CameraID AssemblyLineID API_ENDPOINT AUTH_TOKEN TIME_BETWEEN_REQUESTS
# For Example:
# Allow Upload -> python uploadImages-args.py ../resources/circuitboard/extra_images CAM123456 ASM123456 https://XYZ.amazonaws.com/Prod/getsignedurl allow 0
# Deny Upload -> python uploadImages-args.py ../resources/circuitboard/extra_images CAM123456 ASM123456 https://XYZ.amazonaws.com/Prod/getsignedurl deny 0
# Different Camera ID -> python uploadImages-args.py ../resources/circuitboard/extra_images CAM223456 ASM123456 https://XYZ.amazonaws.com/Prod/getsignedurl allow 0
# Different AssemblyLineId -> python uploadImages-args.py ../resources/circuitboard/extra_images CAM123456 ASM223456 https://XYZ.amazonaws.com/Prod/getsignedurl allow 0

# Example Inputs:
# DIRECTORY = '../resources/circuitboard/extra_images'
# CAMERA_ID = 'CAM123456'
# ASSEMBLY_LINE_ID = 'ASM123456'
# API_ENDPOINT = 'https://XYZ.amazonaws.com/Prod/getsignedurl'
# AUTH_TOKEN = 'allow|deny'
# TIME_BETWEEN_REQUESTS = 3 (seconds)


def main():
    args = sys.argv[1:]
    print('########### Lookout For Vision - Serverless App - Image Uploader ############\n')



    try:
        DIRECTORY = args[0]
        CAMERA_ID = args[1]
        ASSEMBLY_LINE_ID = args[2]
        API_ENDPOINT = args[3]
        AUTH_TOKEN = args[4]
        TIME_BETWEEN_REQUESTS = int(args[5])
        IMAGE_EXTENSION_TYPE = '.jpeg'
        
        print('Image Source Directory: ' + DIRECTORY)
        print('Camera: ' + CAMERA_ID)
        print('AssemblyLine: ' + ASSEMBLY_LINE_ID)
        print('API Endpoint: ' + API_ENDPOINT)
        print('Time Delay: ' + args[5]  + 'seconds')
        print('\nStarting with image upload process....')
        
        file_count_success = 0
        file_count_failure = 0
        
        for file in os.scandir(DIRECTORY):
            if file.is_file():
                file_path = file.path
                if (file_path.endswith(IMAGE_EXTENSION_TYPE)):

                    print('\nUploading image file: ' + file_path)
                    IMAGE_ID = file.name
                    headers = {}
                    headers['authorizationToken'] = AUTH_TOKEN
                    params = {}
                    params['cameraid'] = CAMERA_ID
                    params['assemblylineid'] = ASSEMBLY_LINE_ID
                    params['imageid'] = IMAGE_ID
                    
                    response = requests.request('GET', API_ENDPOINT, headers=headers, params=params)
                    response_json = response.json()

                    print('Response from API Gateway when fetching signed URL: ' + str(response.status_code))

                    if response.status_code == 200:
                        print('Signed URL received - proceeding with image upload...')
                        upload_url = response_json['uploadURL']

                        with open(file_path, 'rb') as file_to_upload:
                            file_content = file_to_upload.read()
                            upload_response = requests.request('PUT', upload_url, data=file_content, headers={'Content-Type': 'image/jpeg'})

                            print('Image upload response: ' +
                                str(upload_response.status_code))
                            if upload_response.status_code == 200:
                                print('Image uploaded successfully...')
                                file_count_success+=1
                            else:
                                print('Image upload failed...')
                                file_count_failure+=1
                    else:
                        print('\nUpload failed - error encountered - ' + response.text)

                    time.sleep(TIME_BETWEEN_REQUESTS)
        print('\nUpload process completed')
        print(str(file_count_success) + ' files uploaded successfully')
        print(str(file_count_failure)  + ' files could not be uploaded')
        
    except Exception as e:
        print(e)
        sys.exit(2)


if __name__ == "__main__":
    main()
