from django.shortcuts import render
from django.http import HttpResponse
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

def add_basket(request, product_id):
    
    if request.user.is_authenticated:
       orders = Card.objects.get(customer_id=request.user, data_placed=False) 
       if len(orders) == 1:
        order = orders[0]
        
        #check if item exists already
        item, _ = CartItem.objects.get_or_create(product_id=product_id, order_id=order) 

        item.product_id = product_id
        item.quantity = item.quantity+1
        item.order_id = order

        item.save()
        return HttpResponse('success', content_type="text/plain") 
    else:
        return HttpResponse('login', content_type="text/plain") 

    return HttpResponse('loginn', content_type="text/plain") 
     
