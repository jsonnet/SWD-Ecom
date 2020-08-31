from django.shortcuts import render
from models import *

def product_list(request):

    # get all products from shop and requesting partner
    products = Product.objects.all()

    return render(request, 'product_list.html', {'products':products})



