import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class Create_New_Note_Test(APITestCase):

    """ Test module for inserting a new Note """

    def setUp(self):

        """ This method has the valid and invalid data """

        self.valid_payload = {
            'title': 'test_neww',
            'description': "test",
            'is_archived': True,
            'remainder': 'Today'
        }
        self.invalid_payload = {
            'title': '',
            'description': False,
            'is_archived': 'no',
            'remainder': True
        }
    url=reverse('addnote')
    @pytest.mark.django_db(transaction=True)
    def test_create_valid_note(self):

        """This method is used to test addnote with valid data """

        response = self.client.post(self.url, self.valid_payload,format='json')
        z = response.json()['success']
        self.assertEqual(z, False)



    # def test_create_invalid_note(self):
    #     response = client.HTTPConnection(
    #         reverse('addnote'),
    #         data=json.dumps(self.invalid_payload),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class get_all_notes(APITestCase):

    """ Test module for inserting a new Note """


    url=reverse('getnotes')
    @pytest.mark.django_db(transaction=True)
    def test_get_all_notes(self):

        """This method is used to test addnote with valid data """

        response = self.client.get(self.url)
        z = response.json()['ex']
        self.assertEqual(z, True)


class AccountTests(APITestCase):
    @pytest.mark.django_db(transaction=True)
    def test_create_account(self):
        """
        Ensure we can create a new  object.
        """
        url = reverse('RestRegistration')
        data = {'username': 'DabApps','email':"nikhillad01@gmail.com",'password':'pass123'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': 'registered Successfully', 'data': {}, 'success': True})

    @pytest.mark.django_db(transaction=True)
    def test_login(self):
        """
        Ensure we can create a new  object.
        """
        url = reverse('rest_login')
        data = {"username": "", "password": ""}
        response = self.client.post(url, data, format='json')
        z=response.json()['success']
        self.assertEqual(z,False)


