"""
* Purpose:  Main project URL file
* @author: Nikhil Lad
* @version: 3.7
* @since: 01-1-2019
"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [


    path('', include('apidemo.urls')),  # Includes App Urls

    path('admin/', admin.site.urls),    # URL for admin panel


]


