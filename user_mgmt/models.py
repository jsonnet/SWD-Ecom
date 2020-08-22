from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User


class UserProfile(AbstractBaseUser):
    # Extend existing django user model


    # The email of the user to log in with
    username = models.EmailField(unique=True, blank=False, error_messages={'unique': "A user with that username already exists."})

    # First name and last name of user
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)

    # Is the email verified initially false
    enabled = models.BooleanField(default=False)

    # A timestamp when this user was created. AUTO-GEN
    datetime_joined = models.DateTimeField(verbose_name='datetime joined', auto_now_add=True)

    # A unique token AUTO-GEN
    activation_token = models.CharField(max_length=30, unique=True)



    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', ]

    def __str__(self):
        return f'{self.user.username}'
