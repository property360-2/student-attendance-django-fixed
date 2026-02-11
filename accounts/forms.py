# [accounts/forms.py]
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class':'input','placeholder':'Enter password'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = 'Incorrect username or password. Please try again.'
        self.error_messages['inactive'] = 'This account is inactive.'

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
