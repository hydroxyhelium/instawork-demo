from .models import UserProfile, TeamProfile
from django.db.models import F


def handle_admin_create(request, member,team_id):
    """
    wrapper function for model_update in admin case
    """
    return model_update(request, member, team_id, True)

def handle_nonadmin_create(request, member, team_id):
    """
    wrapper function for model_update in non-admin case
    """
    return model_update(request, member, team_id, False)

def model_update(request, member,team_id, admin):
    """
    Handles updating TeamProfile records for a given user and team.

    Args:
        - request: The HTTP request object.
        - member: The member for whom the TeamProfile is being updated.
        - team_id: The ID of the team to which the member is being added or updated.
        - admin: The admin status for the member in the team.

    Raises:
        - ValueError: If a TeamProfile with the email_id of the member already exists, indicating a forbidden operation.

    Returns:
        - Creates a new TeamProfile record for the member if it doesn't already exist.
        - Updates the TeamProfile record for the requesting user with the specified team_id and admin status.
    """
    filter_condition_1 = {"email_id":member.email_id}
    query_set = TeamProfile.objects.filter(**filter_condition_1)

    if query_set.exists():
        raise ValueError("error forbidden")

    update_values_new_user = {"admin":admin, "team_id": team_id, "first_name":member.first_name, "last_name":member.last_name, 
    "email_id": member.email_id, "phone_number": member.phone_number}

    TeamProfile.objects.create(**update_values_new_user)

    update_values_original = {"team_id": team_id, "first_name":request.user.first_name, "last_name":request.user.last_name, 
    "email_id": request.user.email, "phone_number": request.user.phone_number, "admin": request.user.admin}
    obj, created = TeamProfile.objects.get_or_create(defaults=update_values_original, **{"email_id": request.user.email})
    
    if(not created):
        obj.save()
