from django.contrib.auth.forms import UserCreationForm

from user_mgmt.models import UserProfile
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    # def __init__(self, *args, **kwargs):
    #     super(UserRegisterForm, self).__init__(*args, **kwargs)
    #
    #     for fieldname in ['password1', 'password2']:
    #         self.fields[fieldname].help_text = None

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
