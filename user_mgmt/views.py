from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.utils.crypto import get_random_string

from .forms import *
from .models import UserProfile

import logging

from django.contrib.auth import get_user_model
User = get_user_model()

#setup logger
logger = logging.getLogger('django')


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
            logger.info(
                             f'Your account {user.username} has been created! Please verify your email /accounts/{user.username}/verify/{token}')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user_mgmt/register.html', {'form': form})


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

#request for resetting a password (/accounts/password-reset)
def reset_pw_req(request):

    form = UserPasswordResetRequestForm(request.POST, request.FILES)
    if form.is_valid():
        
        #retrieve user from form
        username = form.cleaned_data.get('username')

        #check if user exists
        try:
            user: UserProfile = UserProfile.objects.get(username=username)
            #generate token and save it in activation token field
            token = get_random_string(length=32)
            user.activation_token = token
            user.save()

            logger.info('sent password reset link /{}/pw-reset/{}'.format(username, token))

        except User.DoesNotExist:
            pass

        #send message either way
        messages.success(request, 'sent password reset link to mail address if it exists')
        return redirect('login')

    else:
        form = UserPasswordResetRequestForm()

    return render(request, 'user_mgmt/reset_request.html', {'form':form})

def reset_pw(request):
    # TODO Creating a link with a password reset token.
    # get username from from via POST request
    # handle sth to generate a token connected to this user to generate a link

    form = UserPasswordResetForm(request.POST, request.FILES)
    if form.is_valid():
        
        #retrieve user from form
        form_user = form.save(commit=False)

        #now we update the password from the database
        user: UserProfile = UserProfile.objects.get(form_user.username)
        user.set_password(form_user.password)
        user.save()

        messages.success(request, 'changed password')
        return redirect('login')

    else:
        form = UserPasswordResetForm()

    return render(request, 'user_mgmt/reset.html', {'form':form})
