"""
* Purpose: Used to create token
* @author: Nikhil Lad
* @version: 3.7
* @since: 01-1-2019
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) +  six.text_type(user.is_active)
# six to represent text data.
account_activation_token = AccountActivationTokenGenerator()
