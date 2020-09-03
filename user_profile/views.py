from django.shortcuts import render

# Create your views here.
def private_profile(request,email):
    return render(request, 'private_profile.html', {})

def public_store(request, email):
    return render(request, 'public_shop.html', {})
