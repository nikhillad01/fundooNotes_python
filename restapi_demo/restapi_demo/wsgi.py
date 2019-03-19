"""
WSGI config for restapi_demo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application
# import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restapi_demo.settings')
#
# django.setup()

application = get_wsgi_application()
project_folder = os.path.expanduser('~/home/admin1/PycharmProjects/REST/restapi_demo')
load_dotenv(os.path.join('project_folder', '.env'))