from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'base.html')  

def high_air(request):
    return render(request, 'high_air.html')
