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

    def is_valid(self):
        # Skip validation for my_field
        self.fields['email_id'].required = False
        return super().is_valid()


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set sample field values as placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'e.g., john_doe'
        self.fields['first_name'].widget.attrs['placeholder'] = 'e.g., John'
        self.fields['last_name'].widget.attrs['placeholder'] = 'e.g., Doe'
        self.fields['email'].widget.attrs['placeholder'] = 'e.g., john@example.com'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'e.g., 1234567890'

class LoginForm(AuthenticationForm):
    pass