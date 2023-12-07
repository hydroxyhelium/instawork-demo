from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm,LoginForm,AddMemberForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, TeamProfile
import time
import random
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin

from django.db import transaction


from .utils import handle_admin_create,handle_nonadmin_create

def generate_random_number_based_on_timestamp():
    timestamp = int(time.time())
    random_component = random.randint(1, 1000)
    result = int(f"{timestamp}{random_component}")

    return result


@login_required(login_url="login/")
def home(request):
    team_members = []

    with transaction.atomic():
        try:
            user_team_profile = TeamProfile.objects.select_for_update().get(email_id=request.user.email)
            # Retrieve other team members with the same team_id
            team_members = TeamProfile.objects.select_for_update().filter(team_id=user_team_profile.team_id).exclude(email_id=request.user.email)
        except Exception as e:
            pass 

    return render(request, 'teams/list_view.html', {'team_members': team_members})

@login_required(login_url="login/")
def add_member(request):
    if request.method == 'POST':
        
        form = AddMemberForm(request.POST)
        user = UserProfile.objects.get(email=request.user.email)

        if(user.team_id == -1):
            team_id = generate_random_number_based_on_timestamp()
        else:
            team_id = user.team_id

        if form.is_valid():
            filter_condition_1 = {"email":request.user.email, "team_id":-1}
            update_values = {"admin":True}

            UserProfile.objects.filter(**filter_condition_1).update(**update_values)
            user = UserProfile.objects.get(email=request.user.email)
            role = form.cleaned_data['admin']
            
            if(role and user.admin):
                member = form.save(commit=False)
                handle_admin_create(request, member, team_id)
                return redirect('teams:home')

            elif(not role):
                member = form.save(commit=False)
                handle_nonadmin_create(request, member, team_id)

                return redirect('teams:home')

            else:
                return render(request, 'teams/error_template.html', {'error_message': 'You do not have permission to add an admin user.'})

    else:
        form = AddMemberForm()

    return render(request, 'teams/add_member.html', {'form': form})

# @login_required(login_url="login/")
class teamprofile_update(UserPassesTestMixin, UpdateView):
    model = TeamProfile
    template_name = 'teams/teams_update_delete.html'
    form_class = AddMemberForm
    
    def get_success_url(self):
        return redirect("teams:home").url

    def form_valid(self, form):
        existing_profiles = TeamProfile.objects.filter(email_id=self.request.user.email)[0]
        if((not existing_profiles.admin) and (form.cleaned_data['admin'])):
            return self.form_invalid(form)
        
        return super().form_valid(form)

    def test_func(self):
        existing_profiles = TeamProfile.objects.filter(email_id=self.request.user.email)[0]

        if(not self.request.user.is_authenticated):
            return False

        if(existing_profiles.team_id != self.get_object().team_id):
            return False
        
        if(existing_profiles.id == self.get_object().id):
            return False
        
        return True
    
    def get_form_kwargs(self):
        kwargs = super(teamprofile_update, self).get_form_kwargs()
        kwargs['instance'] = self.get_object()  # Pass the instance to the form
        return kwargs
    
# @login_required(login_url="login/")
class teamprofile_delete(UserPassesTestMixin, DeleteView):
    model = TeamProfile
    template_name = 'teams/teams_update_delete.html'

    def get_success_url(self):
        return redirect("teams:home").url
    
    def test_func(self):
        # Check if the user is an admin
        if(not self.request.user.is_authenticated):
            return False
        existing_profiles = TeamProfile.objects.filter(email_id=self.request.user.email)[0]
        if(not existing_profiles.admin):
            return False
        return True

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('teams:home')
    else:
        form = AuthenticationForm()

    return render(request, 'teams/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('teams:home')
    else:
        form = SignUpForm()

    return render(request, 'teams/signup.html', {'form': form})