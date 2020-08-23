from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Email must be set!')
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        return self.get(username=email_)

class UserProfile(AbstractUser):
    # Extend existing django user model
    #user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


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
    activation_token = models.CharField(max_length=32)


    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', ]

    def __str__(self):
        return f'{self.user.username}'


