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
    email_id = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be exactly 10 digits")
    phone_number = models.CharField(validators=[phone_regex], max_length=10)

    def __str__(self):
        return "{self.team_id} {self.first_name} {self.last_name} {self.admin} {self.email_id}"

class UserProfile(AbstractUser):
    email = models.EmailField(primary_key=True)
    admin = models.BooleanField(default=False)
    team_id = models.IntegerField(default=-1)
    phone_number = models.CharField(max_length=13)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be exactly 10 digits")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, unique=True)

    def __str__(self):
        return "{self.team_id} {self.email}"