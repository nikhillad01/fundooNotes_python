# from http import client
# from unittest import TestCase
# import json
# import os
# from django.conf import ENVIRONMENT_VARIABLE
# from django.urls import reverse
# from rest_framework import status
# settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
#
#
# class Create_New_Note_Test(TestCase):
#
#     """ Test module for inserting a new Note """
#
#     def setUp(self):
#
#         """ This method has the valid and invalid data """
#
#         self.valid_payload = {
#             'title': 'test',
#             'description': "test",
#             'is_archived': True,
#             'remainder': 'Today'
#         }
#         self.invalid_payload = {
#             'title': '',
#             'description': False,
#             'is_archived': 'no',
#             'remainder': True
#         }
#
#     def test_create_valid_note(self):
#
#         """This method is used to test addnote with valid data """
#
#         response = client.HTTPConnection(
#             reverse('addnote'),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_create_invalid_note(self):
#         response = client.HTTPConnection(
#             reverse('addnote'),
#             data=json.dumps(self.invalid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)