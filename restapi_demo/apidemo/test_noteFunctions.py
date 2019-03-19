"""
* Purpose:This file contains all the custom created decorators which are
          required in project
* @author: Nikhil Lad
* @version: 3.7
* @since: 11-3-2019
"""
#import pytest
from django.test.client import encode_multipart
from .models import Notes
import django
django.setup()
from rest_framework.test import APIRequestFactory
factory = APIRequestFactory()

#pytestmark = pytest.mark.django_db
class Test_Note_Model:
    def test_save(self):

            data= {"title":"PyTest_checking_note_create",
                "description":"py_description",
                "is_archived":False,
                "trash":False}

            content = encode_multipart('BoUnDaRyStRiNg', data)
            content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
            request = factory.post('/addnote/', content, content_type=content_type)

    def test_invalid_data(self):
        data = {"title": "PyTest_checking_note_create",
                "description": None,
                "is_archived": "some_string",
                "trash": False}

        content = encode_multipart('BoUnDaRyStRiNg', data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        request = factory.put('/addnote/', content, content_type=content_type)


    def test_make_archive(self):
            data={"is_archive":True}
            content = encode_multipart('BoUnDaRyStRiNg', data)
            content_type = 'JSON'
            request = factory.post('/is_archive/', content, content_type=content_type)