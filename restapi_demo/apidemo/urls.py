from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from apidemo import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    #Admin Panel and Index.

    #path('admin/', admin.site.urls),
    path('', views.login_v,name='login_v'),
    #path('api/',include('urls.apidemo')),
    # URLS for REST API

    path('rest_register/', views.Signup,name='rest_register'),  # Registration using REST.
    path('rest_login/', views.LoginView.as_view(), name='rest_login'),       # REST Login.
    path('dash/', include('rest_framework.urls', namespace='rest_framework')),



    # Login,Logout And Registration

    path('user_login/', views.demo_user_login,name='user_login'),
    url(r'^signup/$', views.Signup, name='signup'),
    path('login_v/', views.login_v, name='login_v'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('logout/', views.logout, name='logout'),


    # Reset Password

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



    # Upload Profile Pic
    path('upload_profile/', views.upload_profile, name='upload_profile'),
    path('open_upload_form/', views.open_upload_form, name='open_upload_form'),
    path('profile_page/', views.profile_page, name='profile_page'),


    #Base Template

    path('base/', views.base, name='base'),


    #crop profile picture

    path('crop/', views.crop, name='crop'),
    path('photo_list/', views.photo_list, name='photo_list'),


    path('demo/',views.demo,name='demo'),


    # CRUD Operations

    path('addnote/', views.AddNote.as_view(),name='addnote'),
    #deletenote
    path('delete/<int:id>/',views.deleteN, name='deleteN'),
    #getnotes
    #move_to_trash
    path('move_to_trash/<int:id>/',views.trash, name='move_to_trash'),

    path('getnotes/', views.getnotes.as_view(), name='getnotes'),
    #updatenote
    path('updatenote/<int:pk>/', views.updatenote.as_view(),name='updatenote'),
    path('updateform/<int:pk>/', views.updateform, name='updateform'),

    #updateNotes
    path('updateNotes/<int:pk>/', views.updateNotes, name='updateNotes'),


    #pin_unpin
    path('pin_unpin/<int:pk>/', views.pin_unpin, name='pin_unpin'),


    #trash
    path('trash/<int:pk>/', views.trash, name='trash'),
    #view_trash
    path('view_trash/', views.view_trash.as_view(), name='view_trash'),


    #delete_forever
    path('delete_forever/<int:pk>/', views.delete_forever, name='delete_forever'),

    #is_archived
    path('is_archived/<int:pk>/', views.is_archived, name='is_archived'),
    #View_is_archived
    path('View_is_archived/', views.View_is_archived.as_view(), name='View_is_archived'),


    # Labels
    #add_labels
    path('add_labels/<int:pk>/', views.add_labels, name='add_labels'),
    #map_labels
    path('map_labels/', views.map_labels, name='map_labels'),
    #delete_label
    path('delete_label/<int:pk>/', views.delete_label, name='delete_label'),
    #view_notes_for_each_label
    path('view_notes_for_each_label/<int:pk>/', views.view_notes_for_each_label, name='view_notes_for_each_label'),
    #copy_note
    path('copy_note/<int:pk>/', views.copy_note, name='copy_note'),
    #remove_labels
    path('remove_labels/<int:id>/<int:key>/', views.remove_labels, name='remove_labels'),


    # <a href="{% url 'remove_labels' l.label_id  user.id i.id %}" >&times;</a>

    # Search
    path('search/',views.search,name='search'),

    #reminder
    path('reminder/', views.reminder, name='reminder'),
    path('View_reminder/', views.View_reminder.as_view(), name='View_reminder'),


    #Update
    path('Update/<int:pk>/', views.Update.as_view(), name='Update'),
    #View_reminder



    #change_color
    path('change_color/<int:pk>/', views.change_color, name='change_color'),


    #auto_delete_archive
    path('auto_delete_archive/', views.auto_delete_archive, name='auto_delete_archive'),

    #invite
    path('invite/', views.invite, name='invite'),

    #delete_from_s3
    path('delete_from_s3/', views.delete_from_s3, name='delete_from_s3'),
]


