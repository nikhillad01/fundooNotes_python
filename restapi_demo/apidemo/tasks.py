from __future__ import absolute_import, unicode_literals

import datetime

from celery import task, shared_task
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

from .models import Notes
#from .views import get_token


@shared_task
def task_number_one():
    username='tcelery2'
    password='admin123'
    email='nikhillad01@gmail.com'
    user=User.objects.create(username=username, password=password, email=email)
    user.save()
    return 'first task is running , user created successfully '


@shared_task()
def auto_delete_archive_and_trash(user):

    """ This method is used to automatically delete items from Archive and trash
        Archive Notes : Deleted permanently after 15 days or moved to trash
        Trash Notes : Deleted permanently after 7 days
    """

    try:

        note_list = Notes.objects.filter(~Q(archive_time=None), user_id=user, is_archived=True).values('archive_time','id','trash_time').order_by(
            '-created_time')
        today = datetime.datetime.today().date()  # gets the today's date                                                # gets all the notes who's archive time is not None adn is_archive field is True

        for i in note_list:
                                                        # gets the archive_time for each note and add 15 days to it i.e. end_date
            end_date=i['archive_time'] + datetime.timedelta(days=15)

            notes_to_trash=[]
            if end_date.date()==today:                  # if end date and today's date are equal means 15 days over , then move the note to trash.
                item = Notes.objects.get(id=i['id'])    # gets the note by id
                item.trash=True                         # moves to trash.
                item.save()                             # saves the note.
                notes_to_trash.append(item)


        trash_note_list = Notes.objects.filter(~Q(trash_time=None), user_id=user,trash=True).values(
                                                                                                    'id', 'trash_time').order_by(
                                                                                                    '-created_time')

        notes_to_delete=[]
        for j in trash_note_list:
                                                        # gets the trash_time for each note and add 15 days to it i.e. end_date
            end_date=j['trash_time'] + datetime.timedelta(days=7)
            today=datetime.datetime.today().date()
                                                        # gets the today's date
                                                        # if end date and today's date are equal means 7 days over , then permanently delete the note.
            if end_date.date()==today:
                delete_item = Notes.objects.get(id=j['id'])  # gets the note by id
                notes_to_delete.append(delete_item)
                delete_item.delete()                         # deletes the note

        return notes_to_trash, trash_note_list

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print("Exception", e)