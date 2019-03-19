from django.conf.global_settings import AUTH_USER_MODEL
from django.test import TestCase
import pytest

#from restapi_demo.restapi_demo.settings import INSTALLED_APPS

from .models import RestRegistration        # Model
pytestmark = pytest.mark.django_db          # permit to access database
class TestRegisterModel:
    def test_save(self):
            register = RestRegistration.objects.create(
                username="PyTest",
                password=500,
                confirm_password=500,
                email="nikhillad01@gmail.com"
            )
            assert register.username == "PyTest"
            assert register.password == 500
            assert register.confirm_password == 500
            assert register.email == "nikhillad01@gmail.com"

class SettingsTest(TestCase):
    def test_account_is_configured(self):
       # self.assertTrue('apidemo' in INSTALLED_APPS)
        self.assertTrue('auth.User' == AUTH_USER_MODEL)     # True Condition

        self.assertFalse('apidemo.User' == AUTH_USER_MODEL) # Checks for False value

