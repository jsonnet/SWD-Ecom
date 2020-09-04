from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt


def index(request):
    return render(request, 'base.html')


@xframe_options_exempt
def high_air(request):
    return render(request, 'high_air.html')
