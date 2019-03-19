"""
* Purpose:  Serializers
* @author: Nikhil Lad
* @version: 3.7
* @since: 01-1-2019
"""
from django.forms import forms
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.contrib.auth.models import User
import jwt
from rest_framework import  exceptions
from .models import Notes
User= get_user_model()


class registrationSerializer(serializers.ModelSerializer):
                # Creates an Serializer class with fields from model.


    username=serializers.CharField(max_length=20)
    password=serializers.CharField(style={'input_type': 'password'})
    email=serializers.RegexField(regex=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',required=True)

    class Meta:       # inner class provides a metadata to ModelForm Class.

        model = User                    # Database Model to  store the data in .
        fields=['username',
                'password',
                'email']

    def clean(self):
        cleaned_data = super(registrationSerializer, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match")



class TokenAuthentication(BaseAuthentication, serializers.ModelSerializer):  # provides a way to crrate serializer class with fields in Model.
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:         # inner class provides a metadata to ModelForm Class.
        model = User            # sets Model as User Model.
        fields = ['username',
                  'password']

        def get_model(self):
            return User


        def authenticate_credentials(self, token):

            """This method is used if we pass our token to other app or method
            this will validated if user is valid or not by decoding the token"""

            payload = jwt.decode(token, "SECRET_KEY",algorithm='HS256')     # decodes the token
            username = payload['username']      # gets username from decoded token
            password = payload['password']      # gets password from decoded token
            msg = {'Error': "Token mismatch", 'status': "401"}
            try:

                user = User.objects.get(
                    username=username,
                    password=password,
                    is_active=True
                )

                if not user.token['token'] == token:
                    raise exceptions.AuthenticationFailed(msg)

            except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
                return HttpResponse({'Error': "Token is invalid"}, status="403")
            except User.DoesNotExist:
                return HttpResponse({'Error': "Internal server error"}, status="500")

            return (user, token)

        def authenticate_header(self, request,token):
            return token

class LoginDemoWithRest(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(style={'input_type': 'password'})



class NoteSerializer(serializers.ModelSerializer):
    # Serializer for Notes

	class Meta:
		model = Notes
		fields = ('title','description','is_archived','reminder','trash','user','for_color','is_pinned','collaborate')

