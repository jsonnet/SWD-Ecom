from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.utils.crypto import get_random_string

from google.oauth2 import id_token
from google.auth.transport import requests

from .forms import UserRegisterForm
from .models import UserProfile


def index(request):
    return redirect('login')  # Temporary


# Logs you out and navigates to index
def logout_view(request):
    logout(request)
    messages.success(request, f'You have been logged out')
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.POST:
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():  # valid submit
            user = form.save(commit=False)  # create user but dont save just yet

            token = get_random_string(length=32)
            user.activation_token = token

            email = form.cleaned_data.get('username')  # retrieve form data

            user.save()  # now save user

            # Display message in template
            messages.success(request,
                             f'Your account {user.username} has been created! Please verify your email /accounts/{user.username}/verify/{token}')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user_mgmt/register.html', {'form': form})



def sso_verify_login(request):
    token = 0

    if request.POST:
        token = 0
        # TODO get GET param id_token=

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        CLIENT_ID = '7641991400-s26aepc1u29217cleq028fl74l044cru.apps.googleusercontent.com'
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        email = idinfo['email']
        enabled = idinfo['email_verified']
        first_name = idinfo['family_name']
        last_name = idinfo['sub']

        # TODO create user

    except ValueError:
        # Invalid token
        pass

    return None  #TODO just a get with the username


def verify_user(request, email, token):
    try:
        # Get the user from the email provided
        current_user: UserProfile = UserProfile.objects.get(username=email)
        # obviously request.user does not work as we are not logged in thus AnonymousUser

        if not current_user.enabled and token == current_user.activation_token:
            current_user.enabled = True

            # now update and save user again
            current_user.save()

            return HttpResponse('The user {} has been verified! You can now log in'.format(current_user.username))
    except UserProfile.DoesNotExist:  # the objects can fail with DoesNotExists if a wrong email was provided
        pass

    return HttpResponse('The provided details for {} with {} where wrong or already used {}'.format(email, token))


def reset_pw(request):
    # TODO Creating a link with a password reset token.
    # get username from from via POST request
    # handle sth to generate a token connected to this user to generate a link
    return render(request, 'user_mgmt/reset.html')
