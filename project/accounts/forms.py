from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1', 'password2')

    def send_email(self):
        pass

    def clean_passsword2(self):
        password = User.objects.make_password()
        return password
