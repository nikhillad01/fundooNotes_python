from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restapi_demo.settings')
app = Celery('restapi_demo')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, once={'graceful': True})
def debug_task(*args):
    print('my first task')