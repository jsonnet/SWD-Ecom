from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'base.html')  # TODO change to index file dont use base!! only for testing
