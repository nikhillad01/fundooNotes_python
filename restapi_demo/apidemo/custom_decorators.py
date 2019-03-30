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
from self import self
from .redis_services import redis_info
import jwt


def custom_login_required(function=None,login_url =''):
    try:
        def is_login(request):
            token = redis_info.get_token(self,'token')  # gets the token from redis cache
            if token:
                token = token.decode(encoding='utf-8')  # decodes the token ( from Bytes to str )
                decoded_token = jwt.decode(token, 'secret_key',algorithms=['HS256'])  # decodes JWT token and gets the values Username etc
                user = User.objects.get(username=decoded_token['username']).pk  # gets the user from username
            else:
                return None
            return User.objects.filter(pk=user).exists()     # if user is present in DB.
        actual_decorator = user_passes_test(is_login)           # user_passes_test to check if some test passes or not
        if function:
            return actual_decorator(function)
        else:
            return HttpResponse("Not valid user")
    except (ObjectDoesNotExist, AttributeError, Exception) as e:
       return HttpResponse("Dose not exist")

<<<<<<< HEAD
def custom_Log(function):
    try:
        def wrap(request,*args, **kwargs):
            token = request.META.get('HTTP_AUTHORIZATION')
            if token:
                decoded_token = jwt.decode(token, 'secret_key', algorithms=['HS256'])  # decodes JWT token and gets the values Username etc
                user=User.objects.get(username=decoded_token['username'])
                if user:
                    request.user=user
                else:
                    raise ObjectDoesNotExist
            else:
                return None
            if function:
                return function(request,*args,**kwargs)
            else:
                return HttpResponse("Not valid user")
        return wrap
    except (User.DoesNotExist,ObjectDoesNotExist, AttributeError, Exception) as e:
       return "Dose not exist"
=======
    except (ObjectDoesNotExist,AttributeError ,Exception) as e:
        print('exception occurs',e)

        return redirect(reverse('login_v'))
>>>>>>> master
