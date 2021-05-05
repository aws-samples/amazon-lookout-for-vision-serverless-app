// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
 
// Permission is hereby granted, free of charge, to any person obtaining a copy of this
// software and associated documentation files (the "Software"), to deal in the Software
// without restriction, including without limitation the rights to use, copy, modify,
// merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
// permit persons to whom the Software is furnished to do so.
 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
// INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
// PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
// HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
// OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
// SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'use strict'

// const AWSXRay = require('aws-xray-sdk-core')
// const AWS = AWSXRay.captureAWS(require('aws-sdk'))
const AWS = require('aws-sdk')

AWS.config.update({ region: process.env.AWS_REGION || 'eu-west-1' })
const s3 = new AWS.S3()

// Main Lambda entry point
exports.handler = async (event) => {
  const result = await getUploadURL(event)
  console.log('Result: ', result)
  return result
}

const getUploadURL = async function(event) {
  const randomId = parseInt(Math.random()*100000000)
  let cameraid = "cameraid";
  let assemblylineid = 'assemblylineid';
  let imageid = 'imageid';
  const imageFileName = `IMG${randomId}.jpeg`
  
  // if (event.headers && event.headers["cameraid"]) {
  //   console.log("Received cameraid: " + event.headers["cameraid"]);
  //   cameraid = event.headers["cameraid"];
  // }

  // if (event.headers && event.headers["assemblylineid"]) {
  //     console.log("Received assemblylineid: " + event.headers["assemblylineid"]);
  //     assemblylineid = event.headers["assemblylineid"]
  // }

  // if (event.headers && event.headers["imageid"]) {
  //   console.log("Received imageid: " + event.headers["imageid"]);
  //   imageid = event.headers["imageid"];
  // }

  if (event.queryStringParameters && event.queryStringParameters.cameraid) {
      console.log("Received cameraid: " + event.queryStringParameters.cameraid);
      cameraid = event.queryStringParameters.cameraid;
  }

  if (event.queryStringParameters && event.queryStringParameters.assemblylineid) {
      console.log("Received assemblylineid: " + event.queryStringParameters.assemblylineid);
      assemblylineid = event.queryStringParameters.assemblylineid;
  }

  if (event.queryStringParameters && event.queryStringParameters.imageid) {
    console.log("Received imageid: " + event.queryStringParameters.imageid);
    imageid = event.queryStringParameters.imageid;
  }

  const s3Params = {
    Bucket: process.env.UploadBucket,
    Key:  imageid, //imageFileName,
    ContentType: 'image/jpeg', // U,pdate to match whichever content type you need to upload
    //ACL: 'public-read'     // Enable this setting to make the object publicly readable - only works if the bucket can support public objects
    Metadata: {
      cameraid: cameraid,
      assemblylineid: assemblylineid,
      imageid: imageid
    }
  
  }

  console.log('getUploadURL: ', s3Params)
  return new Promise((resolve, reject) => {
    // Get signed URL
    resolve({
      "statusCode": 200,
      "isBase64Encoded": false,
      "headers": {
        "Access-Control-Allow-Origin": "*"
      },
      "body": JSON.stringify({
          "uploadURL": s3.getSignedUrl('putObject', s3Params),
          "photoFilename": imageid //imageFileName
      })
    })
  })
}
