from django.contrib.auth.forms import UserCreationForm

from user_mgmt.models import UserProfile
from django.forms import ModelForm
from django import forms


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

class UserPasswordResetForm(forms.Form):
    password_new1 = forms.CharField(widget=forms.TextInput(attrs={'type':'password', 'placeholder':'New password',  'class' : 'span'}))
    password_new2 = forms.CharField(widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Confirm new password',  'class' : 'span'}))

    def clean(self):
        # check if form contains fields
        if 'password_new1' in self.cleaned_data and 'password_new2' in self.cleaned_data:
            pass

        return self.cleaned_data

class UserPasswordResetRequestForm(forms.Form):
    username = forms.EmailField(widget=forms.TextInput(attrs={'type':'email', 'placeholder':'Your username',  'class' : 'span'}))

