from .models import UserProfile, TeamProfile
from django.db.models import F


def handle_admin_create(request, member,team_id):
    return model_update(request, member, team_id, True)

def handle_nonadmin_create(request, member, team_id):
    return model_update(request, member, team_id, False)

def model_update(request, member,team_id, admin):
    filter_condition_1 = {"email_id":member.email_id}
    query_set = TeamProfile.objects.filter(**filter_condition_1)

    if query_set.exists():
        raise ValueError("error forbidden")

    update_values_new_user = {"admin":admin, "team_id": team_id, "first_name":member.first_name, "last_name":member.last_name, 
    "email_id": member.email_id, "phone_number": member.phone_number}

    TeamProfile.objects.create(**update_values_new_user)

    ## REDUNDANT
    # filter_condition_2 = {"email":request.user.email}
    # update_values_original = {"team_id": team_id}
    # UserProfile.objects.filter(**filter_condition_2).update(**update_values_original)


    update_values_original = {"team_id": team_id, "first_name":request.user.first_name, "last_name":request.user.last_name, 
    "email_id": request.user.email, "phone_number": request.user.phone_number, "admin": request.user.admin}
    obj, created = TeamProfile.objects.get_or_create(defaults=update_values_original, **{"email_id": request.user.email})
    
    if(not created):
        obj.save()

