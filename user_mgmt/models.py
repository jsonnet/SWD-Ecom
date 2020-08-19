from django.db import models


# Create your models here.
class UserProfile(models.Model):
    # The email of the user to log in with
    username = models.EmailField(db_index=True, unique=True)

    # Password of the user
    password = models.CharField(max_length=30)

    # First name and last name of user
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Is the email verified
    enabled = models.BooleanField(default=False)

    # A timestamp when this user was created. AUTO-GEN
    datetime_joined = models.DateTimeField(auto_now_add=True)

    # FIXME
    # A unique token AUTO-GEN
    activation_token = models.CharField(max_length=30, unique=True)
