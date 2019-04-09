"""
* Purpose:This file contains details about Redis services required

* @author: Nikhil Lad
* @version: 3.7
* @since: 10-3-2019
"""
import this

import jwt
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
import redis
from self import self

r = redis.StrictRedis(host='localhost', port=6379, db=0)   # Redis connection



class redis_info:

    """This class is used to set , get and delete data from Redis cache
            StrictRedis does not provide compatibility for older versions of redis.py
            Do you need backwards compatibility ? Use Redis
    """
    res = {
        'message': 'Something Bad Happened',  # Response Data
        'data': {},
        'success': False
    }

    try:
        def set_token(self, key, value):
             if key and value:                     # adds the data to redis
                r.set(key, value)

             else:
                return print('Not valid')


        def get_token(self, key):

             if key:                               # gets the data out of redis
                value=r.get(key)
                return value
             else:
                 return print({'message':'Invalid detail provided'})

        def get_current_loggedUser(self, key):

             if key:                               # gets the data out of redis
                value=r.get(key)
                return value
             else:
                 return print({'message':'Invalid detail provided'})


        def flush_all(self):
            try:
                r.flushall(asynchronous=False)         # deletes all data from redis cache

            except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception):
                return print({"message": "Something bad happened"})
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)

def set_user_credentials():
    token=redis_info.get_token(self,'token')
    token = token.decode(encoding='utf-8')  # decodes the token ( from Bytes to str )
    decoded_token = jwt.decode(token, 'secret_key',
                               algorithms=['HS256'])  # decodes JWT token and gets the values Username etc
    user = User.objects.get(username=decoded_token['username'])  # gets the user from username
    username=user.username
    # username = username.decode(encoding='utf-8')
    redis_info.set_token(self, decoded_token['username'], username)
    return username

