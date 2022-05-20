from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1', 'password2')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'salutation', 'age', 'sex', 'phone')