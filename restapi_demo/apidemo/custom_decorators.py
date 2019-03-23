"""
* Purpose:This file contains all the custom created decorators which are
          required in project

* @author: Nikhil Lad
* @version: 3.7
* @since: 11-3-2019

"""

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from self import self
from .redis_services import redis_info
import jwt


def custom_login_required(function=None,login_url =''):

    try:
        print('in try')
        def is_login(request):
            print('in method')
            token = redis_info.get_token(self,'token')  # gets the token from redis cache
            if token:
                token = token.decode(encoding='utf-8')  # decodes the token ( from Bytes to str )
                decoded_token = jwt.decode(token, 'secret_key',
                                           algorithms=['HS256'])  # decodes JWT token and gets the values Username etc
                user = User.objects.get(username=decoded_token['username']).pk  # gets the user from username
                print('User is: ',decoded_token['username'])# request.user = user
                print(request)
            else:
                return None


            return User.objects.filter(pk=user).exists()     # if user is present in DB.
        actual_decorator = user_passes_test(is_login)           # user_passes_test to check if some test passes or not

        if function:
            return actual_decorator(function)
        else:
            return HttpResponse("Not valid user")
            #return redirect(reverse('login_v'))
            #return actual_decorator


    except (ObjectDoesNotExist, AttributeError, Exception) as e:
        #print(e)
        print('exception')
        print('exception')
        return HttpResponse("Dose not exist")
        #return redirect(reverse('login_v'))
