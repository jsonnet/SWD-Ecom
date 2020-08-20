from django.contrib.auth import authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth.models import User
from . import models


def index(request):
    return HttpResponse("Hello, accounts. Here should be two buttons for login and register")


def login_view(request):
    return HttpResponse("Login")


# Logs you out and navigates to index
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    # TODO WIP
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('pwd', None)
        first_name = request.POST.get('fname', None)
        last_name = request.POST.get('lname', None)
        user = User.objects.create_user(username=email, password=password)

        if user is not None:
            user.save()

            user_profile = models.UserProfile()
            user_profile.username = email
            user_profile.first_name = first_name
            user_profile.last_name = last_name

            # FIXME random token here
            user_profile.activation_token = 0

            user_profile.user = user
            user_profile.save()
            authenticate(request, user)

            return HttpResponseRedirect(reverse('index'))
    return HttpResponse("New user register! CREATE HTML instead")
