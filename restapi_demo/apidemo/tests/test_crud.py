from http import client
import json

from django.urls import reverse
from rest_framework import status


def setUp(self):


         """ This method has the valid and invalid data """


         valid_payload = {
            'title': 'test',
            'description': "test",
            'is_archived': True,
            'remainder': 'Today'}

         response = client.post(
                reverse('addnote'),
                data=json.dumps(valid_payload),
                content_type='application/json'
         )

         assert (response.status_code, status.HTTP_201_CREATED)