from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import UserProfile, TeamProfile
admin.site.register(UserProfile)
admin.site.register(TeamProfile)