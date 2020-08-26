from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm

from user_mgmt.models import UserProfile


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class UserPasswordResetForm(forms.Form):
    password_new1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password_new2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean(self):
        return self.cleaned_data


class UserPasswordResetRequestForm(forms.Form):
    username = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'placeholder': 'Your email', 'class': 'span'}))
