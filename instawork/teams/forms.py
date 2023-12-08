from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from .models import UserProfile, TeamProfile


class AddMemberForm(ModelForm):
    class Meta:
        model = TeamProfile
        fields = ["first_name", "last_name","email_id", "phone_number", "admin"]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name", 
            "email_id": "Email",
            "phone_number": "Phone Number", 
            "admin": "Admin",
        }


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']

        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name', 
            'phone_number': 'Phone Number', 
        }

class LoginForm(AuthenticationForm):
    pass