from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse

from .forms import UserRegisterForm
from django.utils.crypto import get_random_string

from django.contrib.auth import get_user_model

import logging

# Get an instance of a logger
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
            user_saved = form.save(commit=False)  # save user
            #generate random token for email verification
            token = get_random_string(length=32) 
            user_saved.acivation_token = token

            #get cleaned data
            cleaned_data = form.cleaned_data
            email = cleaned_data.get('username')

            user_saved.save()

            logger.info(get_user_model().objects.all())
            logger.info( f'Your account {email} has been created! Please verify your email /accounts/{email}/verify/{token}')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user_mgmt/register.html', {'form': form})
