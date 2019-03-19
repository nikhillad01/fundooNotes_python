"""
* Purpose:This file contains details about Cloud services required

* @author: Nikhil Lad
* @version: 3.7
* @since: 10-3-2019
"""

import boto3
from django.utils.datastructures import MultiValueDictKeyError

s3 = boto3.client('s3')                                    # connection for S3.

class s3_services:

    def upload_image(request, path, username):

        """This method is used to upload the images to Amazon s3 bucket"""

        if path and username:

            file = open(path, 'rb')  # image to upload with read access

            try:
                s3.upload_fileobj(file, 'fundoo', Key=username)
                print('uploaded successfully')
            except (MultiValueDictKeyError,ValueError,KeyboardInterrupt, Exception):  # handles error if no file is selected while submitting
                print('Exception occurs')
        else:
            print('something bad happened')



    def delete_object_from_s3(request,key):

        """This method is used to delete any object from s3 bucket """

        try:
            if key:
                s3.delete_object(Bucket='fundoo', Key=key)

                print("successfully deleted")
            else:
                 print('key not found')
        except (MultiValueDictKeyError,KeyboardInterrupt,ValueError,Exception) as e:
            print('exception')
