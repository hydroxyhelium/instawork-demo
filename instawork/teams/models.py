from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.

class TeamProfile(models.Model):
    team_id = models.IntegerField(default=-1)
    admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_id = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be exactly 10 digits")
    phone_number = models.CharField(validators=[phone_regex], max_length=10)

    def __str__(self):
        return "{team_id} {first_name} {last_name} {admin} {email_id}"

class UserProfile(AbstractUser):
    email = models.EmailField(primary_key=True)
    admin = models.BooleanField(default=False)
    team_id = models.IntegerField(default=-1)
    phone_number = models.CharField(max_length=13)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be exactly 10 digits")
    phone_number = models.CharField(validators=[phone_regex], max_length=10)

    def __str__(self):
        return "{team_id} {email}"