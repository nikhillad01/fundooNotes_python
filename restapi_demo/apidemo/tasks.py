from __future__ import absolute_import, unicode_literals
from celery import task, shared_task
from django.contrib.auth.models import User


@shared_task
def task_number_one():
    #print('My first task runninggggg')
    username='tcelery2'
    password='admin123'
    email='nikhillad01@gmail.com'
    user=User.objects.create(username=username, password=password, email=email)
    user.save()
    return 'first task is running , user created successfully '