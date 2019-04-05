"""
* Purpose:This file contains all the custom created decorators which are
          required in project
* @author: Nikhil Lad
* @version: 3.7
* @since: 11-3-2019
"""
import pytest
from django.test.client import encode_multipart
from django.urls import reverse
from rest_framework import status
from restapi_demo.apidemo.serializers import get_single_data
from .models import Notes
import django
django.setup()
from rest_framework.test import APIRequestFactory
factory = APIRequestFactory()
from django.test import TestCase,Client
client=Client
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
            request = factory.post('/is_archive/247', content, content_type=content_type)

   # delete_collaborator
    def test_delete_collaborator(self):
            #data={"delete_collaborator":True}
            # content = encode_multipart('BoUnDaRyStRiNg', data)
            # content_type = 'JSON'
            request = factory.post('/delete_collaborator/247')

class get_single_note(TestCase):
    def setUp(self) :
        self.note1=Notes.objects.create(title='testNote1',description='testnote1desc')
        self.note2 = Notes.objects.create(title='testNote2', description='testnote2desc')
        self.note3 = Notes.objects.create(title='testNote3', description='testnote3desc')
        self.note4 = Notes.objects.create(title='testNote4', description='testnote4desc')

    def get_valid_single_note(self):
        response=client.get(reverse('get_data_by_id', pk=self.note1.pk))

        note=Notes.objects.get(pk=self.note1.pk)
        serializer = get_single_data
        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
