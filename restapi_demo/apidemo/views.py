"""
* Purpose:  Project API's
* @author: Nikhil Lad
* @version: 3.7
* @since: 01-1-2019
"""
import json

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, JsonResponse, request
from django.urls import reverse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.contrib.auth import login
from self import self
from .redis_services import redis_info
from .models import Notes
from .forms import SignupForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, authenticate
import jwt
from .serializers import TokenAuthentication, delete_collaborator_serializer, LoginDemoWithRest, get_single_data, \
    delete_single_data_by_id, add_label_serializer, map_label_serializer, extra_functions, update_serializer
from .serializers import registrationSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView, ListAPIView, \
    RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from .forms import PhotoForm
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .serializers import NoteSerializer
from rest_framework import status
from .custom_decorators import custom_login_required
from .models import Labels,Map_labels
from django.db.models import Q
import datetime
from .cloud_services import  s3_services

#current_site = Site.objects.get_current()


def index(request):         # this is homepage.1
    return render(request, 'index.html', {})

def login_u(request):
    return render(request, 'login.html',{})

def login_without(request):
    return render(request, 'rest_framework/vertical.html',{})

def dash(request):      # /dash/
    return render(request, 'dashboard.html',{})

def profile_page(request):
    return render(request, 'profile.html', {})

def logout(request):
    auth.logout(request)
    redis_info.flush_all(self)
    return render(request, 'login.html')

def base(request):
    return render(request, 'in.html')

def open_upload_form(request):
    return render(request, 'fileupload.html', {})

User= get_user_model()          # will retrieve the USER model class.

class UserCreateAPI(CreateAPIView):             # Registration using Rest framework Using User Model.

    serializer_class=registrationSerializer
    queryset = User.objects.all()                  # fields according to User   (adds data to USER model)

class LoginView(ListCreateAPIView):


    serializer_class=LoginDemoWithRest
    queryset = User.objects.all()
    http_method_names = ['post', 'get']      # to use POST method by default it was using GET.
    #method_decorator(require_POST)
    res = {
        'message': 'Something bad happened',
        'data': {},
        'success': False
    }
    def post(self, request):
        try:

                username = request.data['username']
                password = request.data['password']
                # print(username,password)
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        payload = {'username': username,        # creates token using Payload.
                                    'password': password, }
                        jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256')}
                        token=jwt_token['token'].decode(encoding='utf-8')

                        return JsonResponse({'token':token},safe=False)      # returns token as response with success status code.


                    else:
                        return HttpResponse("Your account was inactive.")
                else:
                        print("Someone tried to login and failed.")
                        print("They used username: {} and password: {}".format(username, password))
                        return HttpResponse("Invalid login details given")

        except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)
            return render(request, 'dashboard.html', {})




def Signup(request):

    try:

        print(request.META.get('HTTP_HOST'))
        # print(request.scheme)
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)  # object  hasn't yet been saved to the database.
                user.is_active = False          # user disabled
                user.save()                     # stores in database.
                data = {                        # renders to html with variables
                    #"urlsafe_base64_encode" takes user id and generates the base64 code(uidb64).
                    'user': user,
                    'domain': request.META.get('HTTP_HOST'),
                                #current_site.domain,
                    #'uid': urlsafe_base64_encode(force_bytes(user.pk)),    # encodes
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),  # coz django 2.0.0 to convert it to string
                    'token': account_activation_token.make_token(user),  # creates a token
                }
                message = render_to_string('acc_active_email.html', data)
                mail_subject = 'Activate your Fundoo account.'  # mail subject
                to_email = form.cleaned_data.get('email')       # mail id to be sent to
                email = EmailMessage(mail_subject, message, to=[to_email])   # takes 3 args: 1. mail subject 2. message 3. mail id to send
                email.send()                                    # sends the mail
                return HttpResponse('Please confirm your email address to complete the registration')

        else:
            form = SignupForm()
        return render(request, 'signup.html', {'form': form})       # if  GET request

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)



def activate(request, uidb64, token):

    """  This method is used to activate the user when clicks the email link """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))         # decode to string find the primary key of user
        user = User.objects.get(pk=uid)     # gets the username

        if user and account_activation_token.check_token(user, token):
            user.is_active = True           # enables the user
            user.save()                     # saves to DB.
            return HttpResponsePermanentRedirect(reverse('login_v'))
        else:
            return HttpResponse('Activation link is invalid!')

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

def login_v(request):               # renders to login page.
    try:
        return render(request, 'login.html')
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)




@require_POST
@permission_classes([AllowAny, ])
def demo_user_login(request):

    res = {
        'message': 'Something bad happened',
        'data': {},
        'success': False
    }

    """ This method is used to log in user """

    try:
        if request.POST.get('username') and request.POST.get('password'):
            username = request.POST.get('username')             # takes the username from request
            password = request.POST.get('password')             # takes password from request .

            user = authenticate(username=username, password=password)       # checks if username and password are available in DB.
            if user:
                if user.is_active:
                    login(request, user)
                    payload = {'username': username,
                               'password': password}
                    jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256').decode()}    # creates the token using payload String Token
                    j = jwt_token['token']

                    res['message']="Logged in Successfully"
                    res['success']=True
                    res['data'] =j

                    redis_info.set_token(self, 'token', res['data'])    # set the token to redis


                    return render(request, 'in.html', {'token': res})   # renders to page with context=token

                else:
                    res['message'] = "Your account was inactive."
                    return render(request, 'in.html', res)

            else:
                res['message'] = 'Username or Password is not correct' #Invalid login details
                messages.error(request, 'Invalid login details')
                return render(request, 'login.html', context=res)
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)
        return render(request, 'login.html', context=res)




@require_POST
@login_required
def upload_profile(request):

    """ This method is used to upload a profile picture to S3 bucket """
    try:
                              # calls profile_pic upload method from S3 Upload file.
        messages.success(request, "Profile Pic updated")    # returns success message
        return render(request, 'profile.html')
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)

def crop(request):
    try:
        return render(request,'photo_list.html')
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)



def photo_list(request):

    """This method is used to upload a profile picture with cropping functionality"""

    try:

        if request.method == 'POST':
            token = redis_info.get_token(self, 'token')          # gets the token
            token = token.decode(encoding='utf-8')  # converts bytes to string
            decoded_token = jwt.decode(token, 'secret_key', algorithms=['HS256'])       # decodes JWT token to get values
            user = User.objects.get(username=decoded_token['username'])     # gets the user.

            username = request.POST['username']



            print('in view to upload above valid method')
            #if username==user:          # if username is valid
            form = PhotoForm(request.POST, request.FILES)  # django form
            if form.is_valid():
                print('in valid')
                form.save()  # Saves the form.
                return redirect('photo_list')
            else:
                print('form is not valid')
                messages.error(request,'Please select valid JPEG image')
                #return redirect('photo_list')
                return redirect('getnotes')

        else:
            form = PhotoForm()                  # renders to page with form
            return render(request, 'photo_list.html', {'form': form})
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)

def demo(request):
    try:
        return render(request,'demo.html',{})
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)


@custom_login_required
def delete_from_s3(request):
    res = {
        'message': 'Something Bad Happened',  # Response Data
        'data': {},
        'success': False
    }
    try:
        token = get_token(key='token')

        s3_services.delete_object_from_s3(request, token['username'])  # calls the method from services to delete object from s3 with a key

        res['message']="deleted successfully"
        res['success']=True
        messages.error(request, message=res['message'])
        return redirect(reverse('getnotes'))
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) :
        messages.error(request, message=res['message'])
        return redirect(reverse('getnotes'))


# API to create note
#@login_required
class AddNote(CreateAPIView):   # CreateAPIView used for create only operations.

    """This class is used to create a note with REST """

    serializer_class=NoteSerializer     # serializer to add note(specifies and validate )

    def post(self, request):


        try:

            res = {                                 # Response information .
                'message': 'Something bad happened',
                'data': {},
                'success': False
            }

            serializer = NoteSerializer(data=request.data)  # takes the data from form.
            # check serialized data is valid or not

            if request.data['title'] and request.data['description']:   # if title and description is not provided.


                if serializer.is_valid():
                                                # if valid then save it
                    serializer.save()
                                                # in response return data in json format
                    return HttpResponseRedirect(reverse('getnotes'),content=res)

            else:                              # else return error msg in response
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)
            return redirect(reverse('getnotes'))        # redirects to getnotes view



class getnotes(RetrieveAPIView):
    method_decorator(custom_login_required)
    def get(self, request):

        try:
            print('aUTH @!!@!@!@!@ ',request.META.get('HTTP_AUTHORIZATION'))
        except Exception as e:
            print(e)

        # This method is used to read all notes

        res = {
            'message': 'Something bad happened',    # Response Data
            'data': {},
            'success': False
        }

        """This method is used to read all the notes from database."""

        try:
               # gets all the note and sort by created time
            token=get_token('token')
            user=User.objects.get(username=token['username'])

            note_list = Notes.objects.filter(user_id=user.id,trash=False,is_archived=False,).values().order_by('-created_time')   # shows note only added by specific user.

            new_note_list = Notes.objects.filter(user_id=user.id, trash=False, is_archived=False).values('title',
                                                                                                           'description',
                                                                                                                  )  # shows note only added by specific user.
            stores_id_note = []
            for i in note_list:
                #i=json.dumps(i)
                stores_id_note.append(i['id'])
            collaborators_to_note=Notes.collaborate.through.objects.filter(notes_id__in=stores_id_note).values()


            items=Notes.collaborate.through.objects.filter(user_id=user.id).values()

            collab=[]
            for i in items:
                collab.append(i['notes_id'])


            collab_notes=Notes.objects.filter(id__in=collab).values()

            merged=note_list | collab_notes


            labels = Labels.objects.filter(user=user.id).order_by('-created_time')

            paginator = Paginator(merged, 9)          # Show 9 contacts per page
            page = request.GET.get('page')
            notelist = paginator.get_page(page)

            res['message'] = "All Notes"
            res['success'] = True
            res['data'] =notelist


            data=[]
            for i in new_note_list:
                data.append(i)


            all_labels=Labels.objects.all()
            all_map=Map_labels.objects.all()

            all_users=User.objects.filter(~Q(username=token['username'])).values('username','id')
               # returns list of all user except the one who is requesting it .


            allnotes=[]
            for i in note_list:
                allnotes.append(i)

            #return JsonResponse(allnotes,safe=False)
            return render(request, 'in.html', {'notelist': notelist,'labels':labels,'all_labels':all_labels,'all_map':all_map,'all_users':all_users,'collaborators_to_note': collaborators_to_note})

        except (Notes.DoesNotExist, Labels.DoesNotExist, User.DoesNotExist, ObjectDoesNotExist,KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)



class updatenote(UpdateAPIView):


    """Updates notes  using REST Framework"""

    serializer_class = NoteSerializer       # Serializer

    def put(self, request, pk):
        try:
            """This method is used to update the notes"""
            serializer = NoteSerializer(data=request.data)


            res = {
                'message': 'Something bad happened',    # response information
                'data': {},
                'success': False
            }


            if pk and request.data:
                note = Notes.objects.get(pk=pk)  # checks if primary key is available in DB and gets the data

                if serializer.is_valid():
                    # if valid then save it
                    serializer.save()
                    # in response return data in json format
                    res = {
                        'message': 'Updated Successfully',
                        'data': serializer.data,
                        'success': True
                    }
                    return Response(res, status=status.HTTP_201_CREATED)
                # else return error msg in response
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

        except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)

@custom_login_required
def deleteN(request,id):

    """This method is used to delete the note
    pk: Primary key
    """

    res = {
        'message': 'ID not found',  # response information
        'data': {},
        'success': False
    }
    try:
        if id is None:                              # check is ID is not None
                                                    #raise Exception('ID not found')
            return JsonResponse(res)
        else:
            try:
                item = Notes.objects.get(pk=id)     # checks if note is present of specific id

                item.trash=True
                item.save()
                return redirect(reverse('getnotes'))

            except Exception as e:
                print(e)
                res['message'] = "Note not present for specific ID"
                return JsonResponse(res)
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)

@custom_login_required
def updateform(request,pk):

    # this method is used to open the update note form for particular note

    res = {
        'message': 'ID not found',  # response information
        'data': {},
        'success': False
    }
    try:
        if pk ==None:                      # if Pk is not provided.
            messages.error('Invalid Details')
            return redirect(reverse('getnotes'))
        else:
            note = Notes.objects.get(id=pk)  # gets the note with  PK
            return render(request, 'Notes/update.html', {"note": note})

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        return HttpResponse(e)







@custom_login_required
def updateNotes(request,pk):

    """ This method is used to update the notes
    pk: Primary key

    """
    res = {
        'message': 'ID not found',  # response information
        'data': {},
        'success': False
    }
    try:
        pk_note=request.POST.get('pk_note')
        print('found pk',pk_note)
        pk=pk_note


        if pk is None:                  # if pk is not provided.
            messages.error('Invalid Details')
            return redirect(reverse('getnotes'))


        title=request.POST.get('title')
        update_description=request.POST.get('description')




        note=Notes.objects.get(id=pk_note)       # gets the data with primary key
        print('note',note)

        title=request.POST.get('title')
        description = request.POST.get('description')
                              # changing data of note with form data.
        note.title=title
        note.description=description

        note.save()             # saves the updated data
        return redirect(reverse('getnotes'))

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)


def get_all_labels(user):

    """This method is used to get all the labels added by specific user """
    try:
        if user:
            labels = Labels.objects.filter(user=user).order_by('-created_time')
            return labels
        else:
            return []
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)


def get_all_users(username):

    """This method is used to get all users except current logged-In user """
    try:
        if username:

            all_users = User.objects.filter(~Q(username=username)).values('username', 'id')
            return all_users

        else:
            return []
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)


@custom_login_required
def pin_unpin(request,pk):

    """This method is used to make note pinned or unpinned
     pk: Primary key
     """

    try:
        if pk:
            item = Notes.objects.get(id=pk)         # gets particular item from DB with PK.


            if item.is_pinned == False or item.is_pinned==None:
                item.is_pinned=True         # if item is not pinned or False .. pin it
                item.save()                 # saves to the DB.
                messages.success(request,message='Note pinned')
                return redirect(reverse('getnotes'))
            else:
                item.is_pinned=False            # if item is already pinned , unpin it.
                item.save()
                messages.success(request,message='Note Unpinned')
                return redirect(reverse('getnotes'))
        else:
            messages.error('Invalid Details')
            return redirect(reverse('getnotes'))

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        return HttpResponse("Note not found",e)


@custom_login_required
def trash(request,id):

    """This method is used to push item to trash
    pk: Primary key
    """

    try:
        if id:
            item=Notes.objects.get(id=id)

            if item.trash:
                item.trash = False
                item.save()
                messages.success(request, message='item restored')
                return redirect(reverse('getnotes'))

            elif item.trash==False or item.trash==None:          # if item already in trash restore it.
                item.trash = True  # if trash field is None or False, make note trash
                item.trash_time = datetime.datetime.now()
                item.save()
                messages.success(request, message='Item moved to trash')
                return redirect(reverse('getnotes'))
        else:
            messages.error('Invalid Details')
            return redirect(reverse('getnotes'))

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        return HttpResponse("No item found ",e)



class view_trash(View):

    """This method is used to display all the items which are in trash"""

    @method_decorator(custom_login_required)
    def get(self, request):


        res = {
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }

        """ gets all the  notes which are added by specific user and which are in Trash """

        try:
            note_list = Notes.objects.filter(user=request.user, trash=True).order_by('-created_time')  # shows note only added by specific user.


            paginator = Paginator(note_list, 9)  # Show 9 contacts per page
            page = request.GET.get('page')        # also used as prefix in URL
            notelist = paginator.get_page(page)     # gets data page by page

            res['message'] = "All Trash Notes"
            res['success'] = True
            res['data'] = notelist
            print(notelist)
            labels = get_all_labels(request.user)
            all_users=get_all_users(request.user.username)
            return render(request, 'in.html', {'notelist': note_list,'labels':labels,'all_users':all_users})

        except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)

@custom_login_required
def delete_forever(request, pk):

    """This method is used to permanently delete the note
    pk: Primary key
    """
    res = {
        'message': 'Something bad happened',  # Response Data
        'data': {},
        'success': False
    }

    try:
        if pk:
            item = Notes.objects.get(id=pk)

            item.delete()       # deletes the note permanently
            messages.success(request, message='Item Deleted forever')
            return redirect(reverse('getnotes'))
        else:
            messages.error('Invalid Details')
            return redirect(reverse('getnotes'))

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        return HttpResponse(res)


@custom_login_required
def is_archived(request,pk):

    """This method is used to make note archive
    pk: Primary key
    """

    res = {
        'message': 'Something bad happened',  # Response Data
        'data': {},
        'success': False
    }


    try:
        if pk:
            item = Notes.objects.get(id=pk)

            if item.is_archived:      # if archive field is false or None.
                item.is_archived = False
                item.archive_time = None
                item.save()
                messages.success(request, message='Removed from archived')
                return redirect(reverse('getnotes'))

            elif item.is_archived== False or item.is_archived == None:          # it item is already archived
                item.is_archived = True  # make note archive
                item.archive_time = datetime.datetime.now()
                item.save()
                messages.success(request, message='Item is archived')
                return redirect(reverse('getnotes'))

        else:
            messages.error('Invalid Details')
            return redirect(reverse('getnotes'))

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        return HttpResponse(res)



class View_is_archived(View):

    """This method is used to display all the notes which are archived

    """
    res = {
        'message': 'Something bad happened',  # Response Data
        'data': {},
        'success': False
    }

    @method_decorator(custom_login_required)
    def get(self, request):

        """ Reads the notes by user and archived field"""

        res = {
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }

        """This method is used to read all the notes from database."""

        try:
                  # gets all the note and sort by created time
            note_list = Notes.objects.filter(user=request.user, is_archived=True).order_by('-created_time')  # shows note only added by specific user.


            paginator = Paginator(note_list, 9)  # Show 9 contacts per page
            page = request.GET.get('page')
            notelist = paginator.get_page(page)

            res['message'] = "All Trash Notes"
            res['success'] = True
            res['data'] = notelist

            labels = get_all_labels(request.user)
            all_users = get_all_users(request.user.username)
            return render(request, 'in.html', {'notelist': note_list,'labels':labels,'all_users':all_users})

        except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(res)


@custom_login_required
def add_labels(request,pk):

    res = {
        'message': 'Something bad happened',  # Response Data
        'data': {},
        'success': False
    }

    try:
        if pk and request.POST['label_name']:       # if all details provided
            label_name = request.POST['label_name']
            user = pk
            label=Labels.objects.create(user=User.objects.get(id=user),label_name=label_name)
            label.save()
            messages.success(request, message='Label Created')
            return redirect(reverse('getnotes'))
        else:
            messages.error('Invalid Details')
            return redirect(reverse('getnotes'))
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        return HttpResponse(res,e)


@custom_login_required
def map_labels(request, *args ,**kwargs):

    """This method is used to map labels with each notes """
    #print('In Map Labels @!!@!@!@!@ ', request.META.get('HTTP_AUTHORIZATION'))
    res = {
        'message': 'Something bad happened',  # Response Data
        'data': {},
        'success': False
    }

    try:
        if request.POST['pk'] and request.POST['id'] and request.POST['key']:

            label_id = request.POST['pk']
            user = request.POST['id']
            note_id = request.POST['key']
            # creates the instance with above details provided

            map=Map_labels.objects.create(label_id=Labels.objects.get(id=label_id),user=User.objects.get(id=user),note=Notes.objects.get(id=note_id))
            map.save()
            res = {
                'message': 'label mapped',  # Response Data
                'data': {},
                'success': True
            }
            messages.success(request, message='Label mapped')
            return redirect(reverse('getnotes'))

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        return HttpResponse(res)


@custom_login_required
def delete_label(request,pk):

    """This method is used to delete label
    Param: request, Pk : passed with request"""

    res = {
        'message': 'Something bad happened',  # Response Data
        'data': {},
        'success': False
    }

    try:
        if pk:
            label=Labels.objects.get(id=pk)     # gets the label by id and deletes it
            if label:           # IF LABEL FOUND FOR GIVEN id
                label.delete()
                messages.success(request, message='Label deleted')
                return redirect(reverse('getnotes'))
            else:
                print('Label not found for given id')
                messages.error('Label not found for given id')
                return redirect(reverse('getnotes'))
        else:
            messages.error('Invalid Details')
            return redirect(reverse('getnotes'))

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, ObjectDoesNotExist, Exception) as e:
        messages.error(res['message'])
        return redirect(reverse('getnotes'))



@custom_login_required
def view_notes_for_each_label(request, pk):

    """This method is used to view all notes associated with each label"""

    res = {
        'message': 'Something bad happened',  # Response Data
        'data': {},
        'success': False
    }

    try:

        if pk:            # if pk and id is not None.
            token = get_token(key='token')      # gets the token from redis cache
            if token:
                user = User.objects.get(username=token['username']).pk  # gets the PK of user from token's username

                if user:
                    label_id=pk         # sets the pk and id tp label and user id

                    note_list = Map_labels.objects.filter(user_id=user, label_id=label_id).values('id', 'label_id', 'user_id',
                                                                                                     'note_id')

                    ids = []    # list to store ids of all note_ids associated with particular label and user.
                    for i in note_list:

                        ids.append(i['note_id'])


                    """ id_in  parameter checks for all the ids in list and gets  all the data of it """

                    newnotelist = Notes.objects.filter(id__in=ids).values()

                    paginator = Paginator(note_list, 9)  # Show 9 contacts per page
                    page = request.GET.get('page')
                    notelist = paginator.get_page(page)

                    res['message'] = "All Trash Notes"
                    res['success'] = True
                    res['data'] = notelist
                    labels = get_all_labels(user)
                    all_users = get_all_users(token['username'])
                    return render(request, 'in.html', {'notelist': newnotelist,'labels':labels,'all_users':all_users})

                else:
                    print('user not found')
            else:
                print('token not found')
                return redirect(reverse('login_v'))
        else:
            messages.success(request, message=res['message'])
            return redirect(reverse('getnotes'))

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        messages.success(request, message=res['message'])
        return redirect(reverse('getnotes'))



@custom_login_required
def copy_note(request,pk):

    """This method is used to copy the note
    pk: Primary key
    """

    res = {
        'message': 'Something bad happened',  # Response Data
        'data': {},
        'success': False
    }

    try:

        if pk:                              # if Pk is provided.
            obj = Notes.objects.get(pk=pk)  # gets all the data of note by pk.
            if obj:
                obj.pk = None                   # sets the pk of obj to None so django automatically generates it.
                obj.save()                      # saves the copy of note with new pk.
                res['message'] = "Note copied"
                messages.success(request, message=res['message'])
                return redirect(reverse('getnotes'))
            else:
                messages.error('Note not found')
                return redirect(reverse('getnotes'))
        else:
            messages.error('Invalid Details')
            return redirect(reverse('getnotes'))

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:              # if any exception occurs redirect to getnotes
        messages.success(request, message=res['message'])
        return redirect(reverse('getnotes'))



@custom_login_required
def remove_labels(request,id,key,*args,**kwargs):

    """This method is used to remove the label from particular note"""

    res = {
        'message': 'Something bad happened',  # Response Data
        'data': {},
        'success': False
    }

    try:
        if id and key:      # if all details are provided
            token = get_token(key='token')      # gets the token from redis cache
            user = User.objects.get(username=token['username']).pk  # gets the PK of user from token's username
            if user:
            # gets the specific item .

                item = Map_labels.objects.get(user_id=user, label_id=key, note_id=id)
                item.delete()       # gets the item and delete it.
                return redirect(reverse('getnotes'))
            else:
                print('user not found')

        else:
            res['message']="Invalid details provided"
            messages.error(request,res['message'])
            return redirect(reverse('getnotes'))

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        messages.success(request, message=res['message'])
        return redirect(reverse('getnotes'))


@custom_login_required
def search(request):
    res = {
        'message': 'Invalid details provided',  # Response Data
        'data': {},
        'success': False
    }
    try:
            if request.POST['search_text']:                     # if search field is not none

                token = get_token(self,'token')                          # gets the token from redis cach                         algorithms=['HS256'])  # decodes JWT token and gets the values Username etc
                user = User.objects.get(username=token['username']).pk  # gets the user from username

                if user:
                    search_text = request.POST['search_text']       # get the search text

                    # __contains checks if text is present in a field of model

                    new_notelist=Notes.objects.filter(Q(title__contains=search_text),user=user).values()

                    if new_notelist:       # if note_list is not blank

                        paginator = Paginator(new_notelist, 9)  # Show 9 contacts per page
                        page = request.GET.get('page')
                        notelist = paginator.get_page(page)

                        res['success'] = True
                        res['data'] = notelist
                        data=[]
                        for i in new_notelist:
                            data.append(i)
                        if request.is_ajax:
                            print('ajax request')

                            return render(request, 'in.html', {'not_list': new_notelist})
                        else:print('not ajax')
                    else:
                        res['message']="No results found"
                        print('')
                        messages.error(request, message=res['message'])
                        return redirect(reverse('getnotes'))
                else:
                    print('user not found')

            else:
                res['message']="no data"
                messages.error(request, message=res['message'])
                print('no post')
                return redirect(reverse('getnotes'))

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
         print("Exception---------------",e)
         #res['message']=""
         #messages.error(request, message=res['message'])
         return redirect(reverse('getnotes'))




@custom_login_required
def reminder(request):

    """ This method is used to show reminders to user as notifications """

    res = {
        'message': 'No result found',  # Response Data
        'data': {},
        'success': False
    }

    try:
            token = get_token(key='token')      # gets the token from redis cache

            user = User.objects.get(username=token['username']).pk  # gets the user from username

                                                                        # if request made from User.
            items = Notes.objects.filter(user=user).values()    # Gets all notes  for particular user.

            dates=[]                            # list to store only dates of every Note.
            for i in items:
                if i['reminder']:               # if reminder column has some value
                                                # convert str to DT and append the date to the list
                    dates.append(datetime.datetime.strptime(i['reminder'],"%Y-%m-%d"))


            j=datetime.datetime.today()         # stores today's date

            remind_dates=[]                     # list to store the dates for which reminder is in two days.
            for i in dates:
                if (i-j).days<=2 and (i-j).days>=0:
                    print(i,(i-j).days)         # calculates the difference and stores the value to list
                    remind_dates.append(i)

            new_list=[]                          # list elements has some unwanted values and in Str format
            for i in remind_dates:
                i=datetime.datetime.strftime(i, "%Y-%m-%d")     # converts datetime object to a string.
                i=i[:10]                         # convert and slice to remove unwanted details
                new_list.append(i)

            data=Notes.objects.filter(user=user,reminder__in=new_list).values('title','reminder')

            json_list=[]                         # get all notes with reminder
            # QuerySet to JSON

            for i in data:                       # taking QuerySet data to list
                json_list.append(i)

            return JsonResponse(json_list,safe=False)


    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        messages.error(request, message=res['message'])
        return render(request,'in.html', {})










def get_token(key):
    try:
        if key:

            token = redis_info.get_token(self, key)  # gets the token from redis cache
            token = token.decode(encoding='utf-8')  # decodes the token ( from Bytes to str )
            decoded_token = jwt.decode(token, 'secret_key', algorithms=['HS256'])
            return decoded_token
        else:
            return None
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)


class View_reminder(View):

    """This method is used to display all the notes which has reminder
    """
    res = {
        'message': 'Something bad happened',  # Response Data
        'data': {},
        'success': False
    }



    @method_decorator(custom_login_required)    # method decorator is used for CBV
    def get(self, request):
        #print('request-----------',request.META)
        """ Reads the notes by user and archived field"""

        res = {
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }


        try:
                token = get_token(key='token')      # gets the token from redis cache



                user = User.objects.get(username=token['username']).pk          # gets the user from username


                                                     # gets all the note and sort by created time
                note_list = Notes.objects.filter(~Q(reminder=None), user=user).values().order_by('-created_time')  # shows note only added by specific user.

                                                     # Q used for complex queries ' ~ ' for negative condition

                paginator = Paginator(note_list, 9)  # Show 9 contacts per page
                page = request.GET.get('page')
                notelist = paginator.get_page(page)

                res['message'] = "All Trash Notes"
                res['success'] = True
                res['data'] = notelist
                labels = get_all_labels(user)       # gets all labels created by specific user
                all_users=get_all_users(token['username'])
                return render(request, 'in.html', {'notelist': note_list,'labels':labels,'all_users':all_users})


        except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            messages.error(request,res)
            return redirect(reverse('getnotes'))


@custom_login_required
def change_color(request,pk):

    try:
        res = {
            'message': 'No result found',           # Response Data
            'data': {},
            'success': False
        }
        if pk and request.POST['change_color']:     # if pk and data for change color is not None.

            item = Notes.objects.get(id=pk)         # gets the note with ID

            new_color = request.POST['change_color']

            item.for_color=new_color                # changes color with new color
            item.save()
            res['message'] = "color changed"

            return redirect(reverse('getnotes'))

        else:
            print('No Valid details given')
            return redirect(reverse('getnotes'))


    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)
        messages.error(request, message=res['message'])
        return render(request, 'in.html', {})


@custom_login_required
def auto_delete_archive(request):

    """ This method is used to automatically delete items from Archive and trash
        Archive Notes : Deleted permanently after 15 days or moved to trash
        Trash Notes : Deleted permanently after 7 days
    """

    try:

        token = get_token(key='token')     # gets the token from redis cache

        user=User.objects.get(username=token['username']).pk        # gets the PK of user from token's username



        note_list = Notes.objects.filter(~Q(archive_time=None), user_id=user, is_archived=True).values('archive_time','id','trash_time').order_by(
            '-created_time')
                                                        # gets all the notes who's archive time is not None adn is_archive field is True
        for i in note_list:
                                                        # gets the archive_time for each note and add 15 days to it i.e. end_date
            end_date=i['archive_time'] + datetime.timedelta(days=15)
            today=datetime.datetime.today().date()      # gets the today's date

            if end_date.date()==today:                  # if end date and today's date are equal means 15 days over , then move the note to trash.

                item = Notes.objects.get(id=i['id'])    # gets the note by id
                item.trash=True                         # moves to trash.
                item.save()                             # saves the note.



        trash_note_list = Notes.objects.filter(~Q(trash_time=None), user_id=user,trash=True).values(
                                                                                                    'id', 'trash_time').order_by(
                                                                                                    '-created_time')


        for j in trash_note_list:
            # gets the trash_time for each note and add 15 days to it i.e. end_date
            end_date=j['trash_time'] + datetime.timedelta(days=7)

            today=datetime.datetime.today().date()
            # gets the today's date

            # if end date and today's date are equal means 7 days over , then permanently delete the note.
            if end_date.date()==today:
                delete_item = Notes.objects.get(id=j['id'])  # gets the note by id
                delete_item.delete()                         # deletes the note

        archive_delete=[]
        for i in note_list:
           archive_delete.append(i)

        trash_delete=[]
        for i in trash_note_list:
            trash_delete.append(i)

        return HttpResponse(note_list,trash_note_list)

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print("Exception",e)


#@api_view(['POST'])
@custom_login_required
@require_POST
def invite(request):

    res = {
        'message': 'Something Bad Happened',  # Response Data
        'data': {},
        'success': False
    }

    try:
        if request.POST['email']:

            token = get_token(key='token')
            user = User.objects.get(username=token['username'])

            email_user=request.POST['email']        # gets the email

            data = {
                'user': user,
                'domain': request.META.get('HTTP_HOST'),#current_site.domain,
            }

            message = render_to_string('invite.html', data)
            mail_subject = 'Fundoo Invitation'      # mail subject
            to_email = email_user                   # mail id to be sent to
            email = EmailMessage(mail_subject, message,
                                 to=[to_email])     # takes 3 args: 1. mail subject 2. message 3. mail id to send
            email.send()                            # sends the mail

            res['message']="Invitation sent successfully"
            messages.success(request, message=res['message'])
            return redirect(reverse('getnotes'))

        else:
            res['message']="No values given"
            messages.error(request, message=res['message'])
            return redirect(reverse('getnotes'))

    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception):
        messages.error(request, message=res['message'])
        return redirect(reverse('getnotes'))



# REST API's
class Update(UpdateAPIView):        # UpdateAPIView DRF view , used for update only operations.

    """ This is Used for Collaborator From Card"""

    try:
        serializer_class = NoteSerializer

    except (KeyboardInterrupt,MultiValueDictKeyError,Exception) as e:

        print(e)


    def post(self, request, pk):
        """ This method is used to update  and add collaborator from card """

        res = {
            'message': 'No result found',  # Response Data
            'data': {},
            'success': False
        }

        try:
            if pk and request.data['collaborate']:

                token = get_token(key='token')      # gets the token from redis cache
                logged_in_user = User.objects.get(username=token['username'])

                if logged_in_user.id !=request.data['collaborate']:      # if user tries to collaborate with itself
                    item = Notes.objects.get(id=pk)     # gets the Note

                    collab = request.data['collaborate']    # gets the user if to collaborate
                    user = User.objects.get(id=collab)      # gets the user from ID
                    email_to_send=user.email

                    if Notes.collaborate.through.objects.filter(user_id=user, notes_id=item.id):

                        """ Checks if collaborator is already attached to particular Note """

                        res['message']="Collaborator Already Exists to this note"
                        messages.success(request, message=res['message'])
                        return JsonResponse({'success':False})
                        #return redirect(reverse('getnotes'))

                    else:

                        item.collaborate.add(user)
                        item.save()
                        res['message'] = "Collabrator added successfully"

                        data = {
                            'note_sender': logged_in_user,
                            'domain': request.META.get('HTTP_HOST'),#current_site.domain,
                        }

                        message = render_to_string('Notes/collaborate_notification.html', data)
                        mail_subject = 'shared a note with you'  # mail subject
                        to_email = email_to_send  # mail id to be sent to
                        email = EmailMessage(mail_subject, message,
                                             to=[to_email])  # takes 3 args: 1. mail subject 2. message 3. mail id to send
                        email.send()  # sends the mail
                        messages.success(request, message=res['message'])
                        return JsonResponse({'message': res['message']})
                        #return redirect(reverse('getnotes'))
                else:

                    res['message']='Cannot collaborate to same user '
                    messages.error(request, message=res['message'])
                    return JsonResponse({'message': res['message']})
            else:

                messages.error(request, message=res['message'])
                return JsonResponse({'message': res['message']})
                #return redirect(reverse('getnotes'))

        except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            messages.error(request, message=res['message'])
            return JsonResponse({'mess': res['message']})
            # return render(request, 'in.html', {})

class get_data_by_id(RetrieveAPIView):

        """This API is used to get a single instance data by ID(single note data or all notes by single user)
            Parameter: ID
            ListCreateAPIView: Used for read-write  operations  ,provides get and post method handlers"""

        try:
            serializer_class = get_single_data
        except(ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception):
            print('Serializer Error')

        def post(self, request):
            try:
                res = {
                    'message': 'No valid details provided',  # response information
                    'data': {},
                    'success': False
                }
                if request.data['note_id']:
                                                    # checks if note id is passed
                    item = Notes.objects.filter(id=request.data['note_id']).values()
                    data = []
                    for i in item:
                        data.append(i)
                    return JsonResponse({'Note Data': data}, safe=False)

                elif request.data['user_id']:
                                                    # checks if User id is passed
                    item = Notes.objects.filter(user_id=request.data['user_id']).values()
                    data = []
                    for i in item:
                        data.append(i)
                    return JsonResponse({'All notes by user': data}, safe=False)
                else:
                    return JsonResponse(res)

            except (ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception):
                return JsonResponse({'message': 'Something bad happened'})


class delete_note_by_id(DestroyAPIView):
    try:
        serializer_class = delete_single_data_by_id
        queryset = Notes.objects.all()
    except (ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)

    def delete(self, request, pk):
        try:
            res = {  # Response information .
                'message': 'Something bad happened',
                'data': {},
                'success': False
            }
            if pk:
                note = Notes.objects.get(id=pk)
                if note:
                    note.delete()
                    res['message'] = 'Note deleted successfully'
                    res['success'] = True

                    return JsonResponse(res)
                else:
                    res['message'] = 'Note not found for given ID'
                    return JsonResponse(res)
            else:
                res['message'] = 'ID not provided'
                return JsonResponse(res)
        except (ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)
            return JsonResponse(res)


class delete_collaborator(DestroyAPIView):

    def delete(self, request, user_id, note_id):

        res = {  # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }

        try:
            if user_id and note_id:         # if user id and note id are provided
                item = Notes.collaborate.through.objects.get(user_id=user_id, notes_id=note_id)
                item.delete()
                res['message'] = 'Collaborator Deleted successfully'
                res['success'] = True
                return JsonResponse(res)
            else:
                res['message'] = 'No valid details provided'
                return JsonResponse(res)

        except (Notes.DoesNotExist, ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:

            res['message'] = str(e)
            return JsonResponse(res)

class add_label(CreateAPIView):

    serializer_class = add_label_serializer
    def post(self,request,pk):
        res = {  # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }
        try:

            if pk and request.data['label_name']:       # if pk and label name are provided
                label=Labels.objects.create(user=User.objects.get(id=pk), label_name=request.data['label_name'])
                label.save()
                res['message'] = 'Label created successfully'
                res['success'] = True

                return JsonResponse(res)

            else:
                res['message'] = 'valid data not provided'
                return JsonResponse(res)

        except (Labels.DoesNotExist, ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)
            return JsonResponse(res)

class delete_created_label(DestroyAPIView):
    try:

        queryset = Notes.objects.all()
    except (ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)

    def delete(self, request, pk):
        try:
            res = {                         # Response information .
                'message': 'Something bad happened',
                'data': {},
                'success': False
            }
            if pk:              # if pk is provided
                label = Labels.objects.get(id=pk)       # if label is present
                if label:
                    label.delete()
                    res['message'] = 'Label deleted successfully'
                    res['success'] = True

                    return JsonResponse(res)
                else:
                    res['message'] = 'Label not found for given ID'
                    return JsonResponse(res)
            else:
                res['message'] = 'ID not provided'
                return JsonResponse(res)

        except (Labels.DoesNotExist, ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)
            return JsonResponse(res)

class map_label_with_note(CreateAPIView):
    serializer_class =map_label_serializer
    def post(self, request, note_id, user_id, label_id):
        res = {                                         # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }
        try:
            if note_id and label_id and user_id:

                if User.objects.filter(pk=user_id).exists():    # if user is valid
                    if Notes.objects.filter(pk=note_id, user_id=user_id).exists():

                        # if note is present and created by same user

                        mapped_instance = Map_labels.objects.create(note_id=note_id,user_id=user_id,label_id=Labels.objects.get(id=label_id))
                        mapped_instance.save()
                        res['message'] = 'Label mapped successfully'
                        res['success'] = True
                        return JsonResponse(res)
                    else:
                        res['message'] = 'note not found'
                        return JsonResponse(res)
                else:
                    res['message'] = 'User not found'
                    return JsonResponse(res)

            else:
                res['message'] = 'No valid data provided '
                return JsonResponse(res)

        except (Map_labels.DoesNotExist, ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)
            return JsonResponse(res)

class update_label(UpdateAPIView):
    serializer_class = map_label_serializer
    def post(self, request, label_id, user_id):

        res = {  # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }
        try:
            if label_id and user_id:
                if User.objects.filter(pk=user_id).exists():  # if user is valid and present in DB.
                    label=Labels.objects.get(id=label_id,user_id=user_id)
                    label.label_name=request.data['label_name']
                    label.save()
                    res['message'] = 'Label Edited successfully'
                    res['success'] = True
                    return JsonResponse(res)
                else:
                    res['message'] = 'User not found'
                    return JsonResponse(res)
            else:
                res['message'] = 'No valid details provided'
                return JsonResponse(res)
        except (Labels.DoesNotExist, ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)
            return JsonResponse(res)

class get_noteLabel_list(ListAPIView):
    def get(self,request,note_id):
        res = {  # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }
        try:
            if note_id:
                if Notes.objects.filter(pk=note_id).exists():  # if note is valid and present in DB.
                    labels=Map_labels.objects.filter(note_id=note_id).values()
                    if labels:
                        data=[]
                        for i in labels:
                            data.append(i['label_id_id'])

                        label_names=Labels.objects.filter(id__in=data).values('label_name')

                        data=[]
                        for i in label_names:
                            data.append(i)
                        res['message'] = 'All Labels for note'
                        res['success']= True
                        res['data']= data


                        return JsonResponse(res)
                    else:
                        res['message'] = 'Labels not found'
                        return JsonResponse(res)
                else:
                    res['message'] = 'Note not found'
                    return JsonResponse(res)


            else:
                res['message'] = 'No valid data provided'
                return JsonResponse(res)

        except (Map_labels.DoesNotExist, Labels.DoesNotExist, ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)
            return JsonResponse(res)

class get_colaborator_for_note(ListAPIView):
    def get(self, request, note_id):
        res = {  # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }

        try:
            if note_id and type(note_id)==int:
                if Notes.objects.filter(pk=note_id).exists():  # if note is valid and present in DB.
                    collaborators = Notes.collaborate.through.objects.filter(notes_id=int(note_id)).values('user_id')

                    data= []
                    for i in collaborators:
                        data.append(i['user_id'])
                    collaborator_names= User.objects.filter(id__in=data).values('username')

                    data = []
                    for i in collaborator_names:
                        data.append(i)
                    res['message']='Collaborators for Note'
                    res['data']= data
                    res['success']=True
                    return JsonResponse(res)
                else:
                    res['message'] = 'Note not found'
                    return JsonResponse(res)
            else:
                res['message'] = 'No valid details provided'
                return JsonResponse(res)

        except (User.DoesNotExist, Notes.DoesNotExist, ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)
            return JsonResponse(res)

class get_notes_of_label(ListAPIView):
    def get(self, request, label_id):
        res = {  # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }
        try:
            if label_id:
                if Map_labels.objects.filter(label_id_id=label_id).exists():  # if note is valid and present in DB.
                    labels = Map_labels.objects.filter(label_id_id=label_id).values()
                    if labels:
                        data = []
                        for i in labels:
                            data.append(i['note_id'])

                        notes = Notes.objects.filter(id__in=data).values()

                        data = []
                        for i in notes:
                            data.append(i)
                        res['message'] = 'All notes for label'
                        res['success'] = True
                        res['data'] = data

                        return JsonResponse(res)
                    else:
                        res['message'] = 'Notes not found'
                        return JsonResponse(res)
                else:
                    res['message'] = 'No labels '
                    return JsonResponse(res)


            else:
                res['message'] = 'No valid data provided'
                return JsonResponse(res)

        except (Map_labels.DoesNotExist, Labels.DoesNotExist, ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            print(e)
            return JsonResponse(res)

class make_note_archive(UpdateAPIView):
    serializer_class =extra_functions
    def post(self, request, note_id):

        res = {  # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }
        try:
            if note_id:
                if Notes.objects.filter(pk=note_id).exists():    # if note is valid and present in DB.
                    item=Notes.objects.get(id=note_id)
                    if item.is_archived:
                        item.is_archived=False
                        item.save()
                        res['message']= 'Note removed from archive'
                        res['success']=True
                        return JsonResponse(res)

                    elif item.is_archived==False or item.is_archived==None:
                        item.is_archived=True
                        item.archive_time = datetime.datetime.now()
                        item.save()
                        res['success'] = True
                        res['message'] = 'Note archived'
                        return JsonResponse(res)
                else:
                    res['message'] = 'Note not present for this id'
                    return JsonResponse(res)

            else:
                res['message'] = 'No valid data provided'
                return JsonResponse(res)


        except (Notes.DoesNotExist,  ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            return JsonResponse(res)


class make_note_trash(UpdateAPIView):
    serializer_class =extra_functions
    def post(self,request,note_id):

        res = {  # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }

        try:
            if note_id:
                if Notes.objects.filter(pk=note_id).exists():    # if note is valid and present in DB.

                    item=Notes.objects.get(id=note_id)

                    if item.trash:
                        item.trash=False

                        item.save()
                        res['message']= 'Note removed from trash'
                        res['success']=True
                        return JsonResponse(res)

                    elif item.trash==False or item.trash==None:
                        item.trash=True
                        item.trash_time = datetime.datetime.now()
                        item.save()
                        res['success'] = True
                        res['message'] = 'Note moved to trash'
                        return JsonResponse(res)
                else:
                    res['message'] = 'Note not present for this id'
                    return JsonResponse(res)

            else:
                res['message'] = 'No valid data provided'
                return JsonResponse(res)


        except (Notes.DoesNotExist,  ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            return JsonResponse(res)

class note_pin_unpin(UpdateAPIView):
    serializer_class =extra_functions
    def post(self,request,note_id):

        res = {  # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }

        try:
            if note_id:
                if Notes.objects.filter(pk=note_id).exists():    # if note is valid and present in DB.

                    item=Notes.objects.get(id=note_id)

                    if item.is_pinned:
                        item.is_pinned=False
                        item.save()
                        res['message']= 'Note unpinned'
                        res['success']=True
                        return JsonResponse(res)

                    elif item.is_pinned==False or item.is_pinned==None:
                        item.is_pinned=True
                        item.save()
                        res['success'] = True
                        res['message'] = 'Note pinned'
                        return JsonResponse(res)
                else:
                    res['message'] = 'Note not present for this id'
                    return JsonResponse(res)

            else:
                res['message'] = 'No valid data provided'
                return JsonResponse(res)


        except (Notes.DoesNotExist,  ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            return JsonResponse(res)


class view_archived_notes(ListAPIView):
    def get(self,request,user_id):
        res = {                                                     # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }
        try:
            if user_id:                                             # if user id is provided
                if User.objects.filter(pk=user_id).exists():        # checks if user is valid
                    notes=Notes.objects.filter(user_id=user_id,is_archived=True).values()   # gets the notes for user
                    if notes:           # if found notes
                        data=[]
                        for i in notes:     # adds the data from Queryset to list for JSON conversion
                            data.append(i)
                        res['message'] ='Archived notes'
                        res['success'] = True
                        res['data'] = data
                        return JsonResponse(res)
                    else:
                        res['message'] = 'No archived notes'
                        return JsonResponse(res)
                else:
                    res['message'] = 'User not found'
                    return JsonResponse(res)
            else:
                res['message']='No valid Data provided'
                return JsonResponse(res)

        except (Notes.DoesNotExist,  ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            return JsonResponse(res)

class view_trash_notes(ListAPIView):

    """This API is used to get all the trash notes
    Param: user_id : id of user to get notes of """

    def get(self,request,user_id):
        res = {                                                 # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }
        try:
            if user_id:                                         # if user id is provided
                if User.objects.filter(pk=user_id).exists():    # if user is valid and present in DB.
                    notes=Notes.objects.filter(user_id=user_id, trash=True).values()        # gets all trash notes of user
                    if notes:                                   # if notes are not none
                        data=[]
                        for i in notes:
                            data.append(i)
                        res['message'] ='trash notes'
                        res['success'] = True
                        res['data'] = data
                        return JsonResponse(res)
                    else:
                        res['message'] = 'No trash notes'
                        return JsonResponse(res)
                else:
                    res['message'] = 'User not found'
                    return JsonResponse(res)

            else:
                res['message']='No valid Data provided'
                return JsonResponse(res)

        except (Notes.DoesNotExist,  ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            return JsonResponse(res)

class view_pinned_notes(ListAPIView):
    def get(self,request,user_id):
        res = {                                                 # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }
        try:
            if user_id:                                         # if user id is provided
                if User.objects.filter(pk=user_id).exists():    # if user is valid and present in DB.
                    notes=Notes.objects.filter(user_id=user_id,is_pinned=True).values() # gets all notes which are pinned
                    if notes:                                   # if notes are not none
                        data=[]
                        for i in notes:
                            data.append(i)
                        res['message'] ='pinned notes'
                        res['success'] = True
                        res['data'] = data
                        return JsonResponse(res)
                    else:
                        res['message'] = 'No pinned notes'
                        return JsonResponse(res)
                else:
                    res['message'] = 'User not found'
                    return JsonResponse(res)
            else:
                res['message']='No valid Data provided'
                return JsonResponse(res)

        except (Notes.DoesNotExist,  ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            return JsonResponse(res)

class view_reminder_notes(ListAPIView):
    def get(self,request,user_id):
        res = {                                                  # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }
        try:
            if user_id:                                         # if user if is provided
                if User.objects.filter(pk=user_id).exists():    # if user is valid and present in DB.
                    notes=Notes.objects.filter(~Q(reminder=None), user_id=user_id).values()  # gets all the notes whos reminder is not none
                    if notes:                                     # if notes are not none
                        data=[]
                        for i in notes:
                            data.append(i)
                        res['message'] ='reminder notes'
                        res['success'] = True
                        res['data'] = data
                        return JsonResponse(res)
                    else:
                        res['message'] = 'No reminder notes'
                        return JsonResponse(res)
                else:
                    res['message'] = 'User not found'
                    return JsonResponse(res)
            else:
                res['message']='No valid Data provided'
                return JsonResponse(res)

        except (Notes.DoesNotExist,  ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            res['message'] = 'some exception'
            return JsonResponse(res)

class update_details(UpdateAPIView):
    serializer_class = update_serializer
    def post(self, request, note_id):
        res = {  # Response information .
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }
        try:
            if request.data:
                item = Notes.objects.get(id=note_id)
                if item:
                    item.title=request.data['title']
                    item.description=request.data['description']
                    item.is_archived=request.data['is_archived']
                    item.reminder=request.data['reminder']
                    item.trash=request.data['trash']
                    item.for_color=request.data['for_color']
                    item.save()
                    res['message']= 'Note edited'
                    res['success'] = True
                    return JsonResponse(res)
                else:
                    res['message'] = 'note not found'
                    return JsonResponse(res)
        except (Notes.DoesNotExist,  ObjectDoesNotExist, KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            return JsonResponse(res)

class reminder_notification(RetrieveAPIView):

    """ This method is used to send reminder mails to user  """


    def get(self,request):
        res = {
            'message': 'No result found',  # Response Data
            'data': {},
            'success': False
        }
        try:
                token = get_token(key='token')      # gets the token from redis cache

                user = User.objects.get(username=token['username']).pk  # gets the user from username
                user_email=User.objects.get(id=user)
                                                                            # if request made from User.
                items = Notes.objects.filter(user=user).values()    # Gets all notes  for particular user.

                dates=[]                            # list to store only dates of every Note.
                for i in items:
                    if i['reminder']:               # if reminder column has some value
                                                    # convert str to DT and append the date to the list
                        dates.append(datetime.datetime.strptime(i['reminder'],"%Y-%m-%d"))


                j=datetime.datetime.today()         # stores today's date

                remind_dates=[]                     # list to store the dates for which reminder is in two days.
                for i in dates:
                    if (i-j).days<=3 and (i-j).days>=0:
                                                    # calculates the difference and stores the value to list
                        remind_dates.append(i)

                new_list=[]                          # list elements has some unwanted values and in Str format
                for i in remind_dates:
                    i=datetime.datetime.strftime(i, "%Y-%m-%d")     # converts datetime object to a string.
                    i=i[:10]                         # convert and slice to remove unwanted details
                    new_list.append(i)

                data=Notes.objects.filter(~Q(reminder_notification_flag=True),user=user,reminder__in=new_list).values('id','title','reminder')

                json_list=[]                         # get all notes with reminder
                # QuerySet to JSON

                for i in data:                       # taking QuerySet data to list
                    json_list.append(i)



                for i in json_list:

                    data = {
                        'title': i['title'],
                        'reminder_date':i['reminder'],
                        'domain': request.META.get('HTTP_HOST'),  # current_site.domain,
                    }

                    message = render_to_string('Notes/reminder_notification.html', data)
                    mail_subject = 'Reminder alert !'       # mail subject
                    to_email = user_email.email             # mail id to be sent to
                    email = EmailMessage(mail_subject, message,
                                         to=[to_email])     # takes 3 args: 1. mail subject 2. message 3. mail id to send
                    email.send()                            # sends the mail
                    item=Notes.objects.get(id=i['id'])
                    item.reminder_notification_flag=True
                    item.save()
                    res['message'] = "mail sent successfully"
                return JsonResponse(json_list,safe=False)


        except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
            return JsonResponse(e, safe=False)

