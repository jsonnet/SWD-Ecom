from django.shortcuts import render
from django.http import HttpResponse
from shop.models import *
from shop_mgmt.models import *


def product_list(request):
    # get all products from shop and requesting partner
    products = Product.objects.all()

    return render(request, 'product_list.html', {'products': products})


def basket(request, order_id):
    items = []
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(customer_id=request.user, placed=False)
            try:
                # iterate all items from that order
                cartitems = CartItem.objects.filter(order_id=order)

                for cartitem in cartitems:
                    basketitem = dict()
                    product = Product.objects.get(slug=cartitem.product_id)

                    # add to separate structure that combines everything
                    basketitem['price'] = product.price
                    basketitem['name'] = product.name
                    basketitem['image'] = product.image
                    basketitem['quantity'] = cartitem.quantity
                    basketitem['slug'] = product.slug

                    items.append(basketitem)

            except CartItem.DoesNotExist:
                pass
        except Order.DoesNotExist:
            pass
    return render(request, 'basket.html', {'items': items})


def checkout(request, order_id):
    return render(request, 'checkout.html', None)


def add_basket(request, product_id):
    if request.user.is_authenticated:
        order = Order()

        # create new order if not exists
        try:
            order = Order.objects.get(customer_id=request.user, placed=False)
        except Order.DoesNotExist:
            order.customer_id = request.user
            order.save()

        # check if item exists already
        item = CartItem()
        try:
            item = CartItem.objects.get(product_id=product_id, order_id=order)
        except CartItem.DoesNotExist:
            item.quantity = 0

        item.product_id = product_id
        item.quantity = item.quantity + 1
        item.order_id = order

        item.save()
        return HttpResponse('success', content_type="text/plain")
    else:
        return HttpResponse('login', content_type="text/plain")

    return HttpResponse('loginn', content_type="text/plain")
