from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, accounts.")

def login(request):
    return HttpResponse("login")

def logout(request):
    return HttpResponse("logout!")

def register(request):
    return HttpResponse("New user register!")
