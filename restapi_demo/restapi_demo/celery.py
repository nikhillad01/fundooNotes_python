from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restapi_demo.settings')
app = Celery('restapi_demo')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, once={'graceful': True})
def debug_task():
    print('my 22323 task')

@shared_task
def print_something():
    print('Helloo')

