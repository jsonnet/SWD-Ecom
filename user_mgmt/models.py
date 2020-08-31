from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class UserAccountManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None):
        if not username:
            raise ValueError('User must be set!')

        user = self.model(username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password):
        user = self.create_user(username, first_name, last_name, password)
        user.is_staff = True  # access to admin panel
        user.is_superuser = True  # access to perms in admin panel
        user.enabled = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractUser):
    # The email of the user to log in with
    username = models.EmailField(unique=True, blank=False,
                                 error_messages={'unique': "A user with that username already exists."})

    # First name and last name of user
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)

    # Is the email verified initially false
    enabled = models.BooleanField(default=False)

    # A timestamp when this user was created. AUTO-GEN
    datetime_joined = models.DateTimeField(verbose_name='datetime joined')

    # A unique token
    activation_token = models.CharField(max_length=32)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    def __str__(self):
        return self.username


class PWResetToken(models.Model):
    # The email of the user to log in with
    # username = models.EmailField(unique=True, blank=False)
    # Relationship model for security reasons
    username = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    token = models.CharField(max_length=33)

    def __str__(self):
        return self.username.username


# Fire if instance of UserProfile is being saved
@receiver(pre_save, sender=UserProfile)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance._state.adding is True:
        # Creating User
        instance.is_active = instance.enabled  # for registration
    else:
        # Updating User
        instance.is_active = instance.enabled  # for verify
        instance.date_joined = instance.datetime_joined  # make it neater
        pass

