from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from .models import UserProfile, TeamProfile, TempUser


class AddMemberForm(ModelForm):
    # ROLE_CHOICES = (
    #     ('admin', 'Admin'),
    #     ('non_admin', 'Non-Admin'),
    # )

    # role = forms.ChoiceField(choices=ROLE_CHOICES)

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
    # Customize fields if needed
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']

        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name', 
            'phone_number': 'Phone Number', 
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        print("hello")
        filter_condition_1 = {'email':user.email}

        existing_profiles = TempUser.objects.filter(email_id=user.email)
        team_id = -1
        admin = False
        if existing_profiles.exists():
            existing_profile = existing_profiles[0]
            team_id = existing_profile.team_id
            admin = existing_profile.admin

        update_values = {'first_name': user.first_name, 'last_name': user.last_name, 'password': user.password, 'temp': False, 'username': user.username, 
        'team_id': team_id, 'admin': admin, 'phone_number': user.phone_number}

        instance, created = UserProfile.objects.update_or_create(defaults=update_values, **filter_condition_1)

        return user

class LoginForm(AuthenticationForm):
    pass