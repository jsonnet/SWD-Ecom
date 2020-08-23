from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.utils.crypto import get_random_string

from .forms import UserRegisterForm


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

            # generate random token for email verification
            token = get_random_string(length=32)
            user.acivation_token = token

            email = form.cleaned_data.get('username')  # retrieve form data

            user.save()  # now save user

            # Display message in template
            messages.success(request,
                             f'Your account {user.username} has been created! Please verify your email /accounts/{user.username}/verify/{token}')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user_mgmt/register.html', {'form': form})


def verify_user(request, email, token):
    # TODO
    print(email)
    print(token)
    pass
