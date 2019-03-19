"""
* Purpose:  Forms

* @author: Nikhil Lad
* @version: 3.7
* @since: 01-2-2019

"""
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from image import settings
from requests import request
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from PIL import Image
from django import forms
from .models import Photo
from .cloud_services import s3_services

User= get_user_model()

class LoginForm(forms.ModelForm):
    model=User
    class Meta:
        fields=['username','password',]



class SignupForm(UserCreationForm):     # inheriting user-creation form to create form with following fields

    email=forms.RegexField(regex=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class loginForm(AuthenticationForm):     # inheriting user-creation form to create form with following fields
    class Meta:
        model = User
        fields = ('username','password')

    def save(self, commit=True):
        user = super(loginForm, self).save(commit=False)

        if commit:
            user.save()
        return user

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Select a file')






class PhotoForm(forms.ModelForm):
    username = forms.CharField(required=True,label='Username',widget=forms.TextInput(attrs={'placeholder': 'Username '}))
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height', )


    """ X coordinate, Y coordinate, height and width of the cropping box """

    def save(self):
        username = self.cleaned_data.get('username')    # username to save image for particular user.
        print('username-----------',username)
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')      # X coordinate
        y = self.cleaned_data.get('y')      # X coordinate
        w = self.cleaned_data.get('width')  # width of cropping box
        h = self.cleaned_data.get('height')  # height of cropping box

        # print(x,y,w,h)
        # print(photo)
        # print('taken measures ')
        image = Image.open(photo.file).convert('RGB')              # opens image file using Pillow library
        #print('take image object')
        #image.show()
        cropped_image = image.crop((x, y, w+x, h+y))        # crops image with x,y,w,h
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)  # resize cropped image.
        resized_image.save(photo.file.path)
        path=photo.file.path                    # gets the image path.
        s3_services.upload_image(request, path, username)      # calls method to upload pic to S3.


        return photo

    def clean_photo(self):
        #image_file = self.cleaned_data.get('photo')
        #super(PhotoForm, self)
        try:
            image_file = super(PhotoForm, self)
            if not image_file.name.endswith(".png",".jpeg",".jpg"):
                #raise forms.ValidationError("Only .jpeg image accepted")
                messages.error(request, 'Please select valid file')
                return redirect('photo_list')
            return image_file

        except Exception as e:
            print(e)
    # def clean_photo(self):
    #     photo = self.cleaned_data.get(['photo'])
    #     print('cleaned ',photo)
    #     if photo:
    #         print('in if loop')
    #         format = Image.open(photo.file).format
    #         print('format ',format)
    #         photo.file.seek(0)
    #         if format in settings.VALID_IMAGE_FILETYPES:
    #             return photo
    #     raise forms.ValidationError('error')