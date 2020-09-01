from django.shortcuts import render
from shop.models import *
from shop_mgmt.models import *


def product_list(request):
    # get all products from shop and requesting partner
    products = Product.objects.all()

    return render(request, 'product_list.html', {'products': products})


def basket(request, order_id):

    return render(request, 'basket.html', None)


def checkout(request, order_id):

    return render(request, 'checkout.html', None)
