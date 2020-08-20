from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # Extend existing django user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The email of the user to log in with
    username = models.EmailField(unique=True, blank=False, error_messages={
            'unique': "A user with that username already exists."
        })

    # Password of the user (already exists)
    # password = models.CharField(max_length=30, blank=False)

    # First name and last name of user
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)

    # Is the email verified initially false
    user.is_active = enabled = models.BooleanField(default=False)

    # A timestamp when this user was created. AUTO-GEN
    datetime_joined = models.DateTimeField(auto_now_add=True)

    # A unique token AUTO-GEN
    activation_token = models.CharField(max_length=30, unique=True)
