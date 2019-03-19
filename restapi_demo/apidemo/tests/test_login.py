# # from demo_user
# from django.contrib.auth.models import User
# import os
# import pytest
#
# pytestmark = pytest.mark.django_db  # allows database access
#
#
# def test_demo_user_login(client):
#     user = User.objects.create(username="chiragninja", password='pushkarnikhil123')
#     response = client.post('http://127.0.0.1:8000/rest_login/',
#                            {'username': 'chiragninja', 'password': 'pushkarnikhil123'})
#     assert response.status_code == 200  # response with success status code.
#
#
