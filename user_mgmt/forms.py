from django.contrib.auth.forms import UserCreationForm

from user_mgmt.models import UserProfile


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
