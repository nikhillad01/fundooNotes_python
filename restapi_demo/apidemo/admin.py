"""This file has details of models to show in admin panel """


from django.contrib import admin
from .models import RestRegistration,Notes
# Register your models here.
admin.site.register(RestRegistration)
admin.site.register(Notes)