from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# User = settings.AUTH_USER_MODEL

from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin


# FIXME needs redoing asap!
class UserAccountManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None):
        if not username:
            raise ValueError('User must be set!')
        user = self.model(username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # FIXME not working right now as of is_Admin
    def create_superuser(self, username, first_name, last_name, password):
        user = self.create_user(username, first_name, last_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractUser):
    # The email of the user to log in with
    username = models.EmailField(unique=True, blank=False,
                                 error_messages={'unique': "A user with that username already exists."})

    # First name and last name of user
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)

    # Is the email verified initially false # TODO
    AbstractUser.is_active = enabled = models.BooleanField(default=False)

    # A timestamp when this user was created. AUTO-GEN
    datetime_joined = models.DateTimeField(verbose_name='datetime joined', auto_now_add=True)

    # A unique token
    activation_token = models.CharField(max_length=32)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    is_admin = False

    def __str__(self):
        return self.username

    # TODO
    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

