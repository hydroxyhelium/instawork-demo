from .models import UserProfile, TeamProfile, TempUser
from django.db.models import F


def handle_admin_create(request, member,team_id):

    filter_condition_1 = {"email_id":member.email_id}
    update_values_new_user = {"admin":True, "team_id": team_id, "first_name":member.first_name, "last_name":member.last_name, 
    "email_id": member.email_id, "phone_number": member.phone_number}

    instance, created = TeamProfile.objects.update_or_create(defaults=update_values_new_user, **filter_condition_1)

    filter_condition_2 = {"email":request.user.email}
    update_values_original = {"team_id": team_id}
    UserProfile.objects.filter(**filter_condition_2).update(**update_values_original)


    update_values_original = {"team_id": team_id, "first_name":request.user.first_name, "last_name":request.user.last_name, 
    "email_id": request.user.email, "phone_number": request.user.phone_number}
    obj, created = TeamProfile.objects.get_or_create(defaults=update_values_original, **filter_condition_2)
    
    if(not created):
        obj.team_id = team_id
        obj.save()

    create_temp_user(member, team_id, True)

def create_temp_user(member, team_id, admin):
    existing_profiles = UserProfile.objects.filter(email=member.email_id)
    if existing_profiles.exists():
        ## no need for us to create temp user
        return 
    other_fields = {"team_id":team_id, "admin": admin}
    print(team_id)
    user_profile = TempUser.objects.create(email_id=member.email_id, **other_fields)

def handle_nonadmin_create(request, member, team_id):
    
    filter_condition_1 = {"email_id":member.email_id}
    update_values_new_user = {"admin":False, "team_id": team_id, "first_name":member.first_name, "last_name":member.last_name, 
    "email_id": member.email_id, "phone_number": member.phone_number}

    instance, created = TeamProfile.objects.update_or_create(defaults=update_values_new_user, **filter_condition_1)

    filter_condition_2 = {"email":request.user.email}
    update_values_original = {"team_id": team_id}
    UserProfile.objects.filter(**filter_condition_2).update(**update_values_original)


    filter_condition_2 = {"email_id":request.user.email}

    update_values_original = {"team_id": team_id, "first_name":request.user.first_name, "last_name":request.user.last_name, 
    "email_id": request.user.email, "phone_number": request.user.phone_number}
    obj, created = TeamProfile.objects.get_or_create(defaults=update_values_original, **filter_condition_2)
    
    if(not created):
        obj.team_id = team_id
        obj.save()

    create_temp_user(member, team_id, False)