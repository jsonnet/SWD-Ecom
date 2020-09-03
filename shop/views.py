import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from shop.models import *
from shop_mgmt.models import *


def product_list(request):
    # get all products from shop and requesting partner
    products = Product.objects.all()

    return render(request, 'product_list.html', {'products': products})


@login_required
def basket(request, order_id):
    items, total_count, already_placed = get_basket_items(order_id, request)

    return render(request, 'basket.html',
                  {'items': items, 'item_total': total_count, 'order_id': order_id, 'placed': already_placed})


# FIXME need default function same as basket!!
@login_required
def checkout(request, order_id):
    # If we actually checkout
    if request.method == "POST":
        # TODO create a new address object and save
        #  create a new payment object
        #  add both to the order object
        #  change placed and time in order object
        #  send success message
        #  also check again if every product was still available
        params = json.loads(request.body.decode('utf-8'))
        print(json.loads(request.body.decode('utf-8')))
        print(request.user)

        street = params.get('street')
        add_info = params.get('additional_info')
        zip_city = params.get('city')  # needs to be split
        country = params.get('country')
        payment = params.get('payment')
        amount = calc_total(order_id, request.user)

        # TODO create objects

        messages.error(request,
                       'One or more items are currently not available anymore')  # this will show on the next request

        return HttpResponse("success")

    items, total_count, placed = get_basket_items(order_id, request)
    address = None
    try:
        address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        pass

    return render(request, 'checkout.html',
                  {'items': items, 'item_total': total_count, 'order_id': order_id, 'address': address,
                   'placed': placed, 'user': request.user})


def get_basket_items(order_id, request):
    placed = False
    items = []
    total_count = 0
    try:
        order = Order.objects.get(customer_id=request.user, pk_x=order_id)
        # iterate all items from that order
        cartitems = CartItem.objects.filter(order_id=order)

        for item in cartitems:
            basketitem = dict()
            product = Product.objects.get(slug=item.product_id)

            # add to separate structure that combines everything
            if item.quantity > 0:
                basketitem['price'] = product.price
                basketitem['name'] = product.name
                basketitem['image'] = product.image
                basketitem['quantity'] = item.quantity
                basketitem['avaquantity'] = product.count
                basketitem['slug'] = product.slug

                items.append(basketitem)
            total_count += item.quantity

        placed = order.placed

    except CartItem.DoesNotExist:
        pass
    except Order.DoesNotExist:
        pass
    except Product.DoesNotExist:
        pass
    return items, total_count, placed


def basket_default(request):
    pk_x = -1
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(customer_id=request.user, placed=False)
            pk_x = order.pk_x
        except Order.DoesNotExist:
            pass

    return basket(request, pk_x)


# CDN ENDPOINT

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
        return redirect('basket-default')
    else:
        return HttpResponse('login', content_type="text/plain")


def remove_basket(request, product_id):
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
            item.quantity = item.quantity - 1
            item.order_id = order
            print(item.quantity)
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()

        except CartItem.DoesNotExist:
            pass

    return HttpResponse('done', content_type="text/plain")


def basket_total(request, order_id):
    total = 0.0
    if request.user.is_authenticated:
        total = calc_total(order_id, request.user)

    return HttpResponse(round(total, 2), content_type="text/plain")


def calc_total(order_id, user):
    total = 0.0
    try:
        order = Order.objects.get(customer_id=user, pk_x=order_id)
        cartitems = CartItem.objects.filter(order_id=order)

        for cartitem in cartitems:
            product = Product.objects.get(slug=cartitem.product_id)
            total += float(product.price) * float(cartitem.quantity)

    except CartItem.DoesNotExist:
        pass
    except CartItem.DoesNotExist:
        pass
    except Order.DoesNotExist:
        pass
    return total


def basket_total_default(request):
    order_id = -1
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(customer_id=request.user, placed=False)
            order_id = order.pk_x
        except Order.DoesNotExist:
            pass

    return basket_total(request, order_id)
