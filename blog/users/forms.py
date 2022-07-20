from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile, Post


class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name',
            'email',
            'birthday',
        ]


class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name',
            'email',
            'bio',
            'profile_photo',
            'cover_photo'
        ]


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'description']