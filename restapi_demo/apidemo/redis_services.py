"""
* Purpose:This file contains details about Redis services required

* @author: Nikhil Lad
* @version: 3.7
* @since: 10-3-2019
"""


from django.utils.datastructures import MultiValueDictKeyError
import redis


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


        def flush_all(self):
            try:
                r.flushall(asynchronous=False)         # deletes all data from redis cache
            except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception):
                return print({"message": "Something bad happened"})
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)

