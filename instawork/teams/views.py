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
from django.core.exceptions import PermissionDenied
from django.contrib import messages

def generate_random_number_based_on_timestamp():
    """Generates a random number based on the current timestamp.

    Returns:
        An integer representing the random number generated.
    """
    timestamp = int(time.time())
    random_component = random.randint(1, 1000)
    result = int(f"{timestamp}{random_component}")

    return result


@login_required(login_url="login/")
def home(request):
    """Renders the home page for a team.
    Retrieves the team ID of the logged-in user and displays a list of other team members with the same team ID.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML template that displays a list of team members.
    """
    team_members = []

    with transaction.atomic():
        try:
            user_team_profile = TeamProfile.objects.select_for_update().get(email_id=request.user.email)
            print(user_team_profile.team_id)
            if(user_team_profile.team_id != -1):
                team_members = TeamProfile.objects.select_for_update().filter(team_id=user_team_profile.team_id)
            else:
                team_members = [user_team_profile]
        except Exception as e:
            print(e)
            pass 

    return render(request, 'teams/list_view.html', {'team_members': team_members})

@login_required(login_url="login/")
def add_member(request):
    """
    Add a team member to the user's team with optional admin privileges.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the home page upon successful addition; otherwise, displays error messages or templates.
    """
    if request.method == 'POST':
        
        form = AddMemberForm(request.POST)
        team_id = -1
        user_admin = True

        with transaction.atomic():
            try:
                user_team_profile = TeamProfile.objects.select_for_update().get(email_id=request.user.email)
                # Retrieve other team members with the same team_id
                team_id = user_team_profile.team_id
                user_admin = user_team_profile.admin
            except Exception as e:
                print(e)
                pass 

        if(team_id == -1):
            team_id = generate_random_number_based_on_timestamp()

        if form.is_valid():
            role = form.cleaned_data['admin']
            if(role and user_admin):
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

class teamprofile_update(UserPassesTestMixin, UpdateView):
    """
    UpdateView for modifying TeamProfile.

    Args:
        - UserPassesTestMixin: Mixin to check if the user passes the test_func before allowing access.
        - UpdateView: Django's generic view for handling updating of an object.

    Returns:
        Redirects to the home page upon successful update;
    """
    model = TeamProfile
    template_name = 'teams/teams_update_delete.html'
    form_class = AddMemberForm
    
    def get_success_url(self):
        return redirect("teams:home").url

    def form_valid(self, form):
        existing_profiles = TeamProfile.objects.filter(email_id=self.request.user.email).first()
        query_set = TeamProfile.objects.filter(email_id=form.cleaned_data['email_id'])

        if query_set.exists() and not(query_set[0].email_id == self.get_object().email_id) and not(query_set[0].team_id == -1):
            # You are not allowed to add members from other teams
            # messages.error(self.request, "Operation failed: You cannot add members from other teams.")
            print(self.get_object().email_id)
            return self.form_invalid(form)

        if not existing_profiles.admin and form.cleaned_data['admin']:
            # Non-admin user trying to upgrade privilege
            # messages.error(self.request, "Operation failed: Non-admin users cannot upgrade privileges.")
            return self.form_invalid(form)

        if not existing_profiles.admin and self.get_object().admin and not form.cleaned_data['admin']:
            # Non-admin user trying to downgrade privilege
            # messages.error(self.request, "Operation failed: Non-admin users cannot downgrade privileges.")
            return self.form_invalid(form)

        messages.success(self.request, "Operation successful: Form submitted successfully.")
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
    
    # def handle_no_permission(self):
    #     raise PermissionDenied("You don't have the right permission or the member assigned to some other team.")
    
    def get_form_kwargs(self):
        kwargs = super(teamprofile_update, self).get_form_kwargs()
        kwargs['instance'] = self.get_object()  # Pass the instance to the form
        return kwargs

class teamprofile_delete(UserPassesTestMixin, DeleteView):
    """
    DeleteView subclass for deleting a TeamProfile instance.

    Args:
        - UserPassesTestMixin: Mixin to check if the user passes the test_func before allowing access.
        - DeleteView: Django's generic view for handling deletion of an object.

    Returns:
        - URL to redirect to upon successful deletion, pointing to the 'teams:home' route.
    """
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
    """
    Handles user authentication and login.

    Args:
        - request: The HTTP request object.

    Returns:
        - If the request method is POST and the submitted form is valid, authenticates the user and redirects to 'teams:home'.
        - If the request method is GET, renders the login form.
    """
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
    """
    Handles user registration and signup.

    Args:
        - request: The HTTP request object.

    Returns:
        - If the request method is POST and the submitted signup form is valid, creates a new user, logs them in, and redirects to 'teams:home'.
        - If the request method is GET, renders the signup form.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            update_values_original = {"team_id": -1, "first_name":user.first_name, "last_name":user.last_name, 
    "email_id": user.email, "phone_number": user.phone_number, "admin": True}
            obj, created = TeamProfile.objects.get_or_create(defaults=update_values_original, **{"email_id": user.email})
            login(request, user)
            return redirect('teams:home')
    else:
        form = SignUpForm()

    return render(request, 'teams/signup.html', {'form': form})