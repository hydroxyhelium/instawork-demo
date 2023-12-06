from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.

class TeamProfile(models.Model):
    team_id = models.IntegerField(default=-1)
    admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_id = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13)

    def __str__(self):
        return "{team_id} {first_name} {last_name} {admin} {email_id}"

class TempUser(models.Model):
    team_id = models.IntegerField(default=-1)
    admin = models.BooleanField(default=False)
    email_id = models.EmailField(unique=True)

    def __str__(self):
        return "{self.team_id} {self.email_id}"

class UserProfile(AbstractUser):
    email = models.EmailField(primary_key=True)
    admin = models.BooleanField(default=False)
    team_id = models.IntegerField(default=-1)    
    temp = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=13)

    def __str__(self):
        return "{team_id} {email}"