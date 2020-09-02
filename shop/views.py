from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from shop.models import *
from shop_mgmt.models import *


def product_list(request):
    # get all products from shop and requesting partner
    products = Product.objects.all()

    return render(request, 'product_list.html', {'products': products})


# TODO display based on order_id and customer
#  he can view all his already placed baskets
#  checkout button should then be disabled!
@login_required
def basket(request, order_id):
    items = []
    total_count = 0
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(customer_id=request.user, pk_x=order_id)
            try:
                # iterate all items from that order
                cartitems = CartItem.objects.filter(order_id=order)

                for cartitem in cartitems:
                    basketitem = dict()
                    product = Product.objects.get(slug=cartitem.product_id)

                    # add to separate structure that combines everything
                    if cartitem.quantity > 0:
                        basketitem['price'] = product.price
                        basketitem['name'] = product.name
                        basketitem['image'] = product.image
                        basketitem['quantity'] = cartitem.quantity
                        basketitem['slug'] = product.slug

                        items.append(basketitem)
                    total_count += cartitem.quantity

            except CartItem.DoesNotExist:
                pass
        except Order.DoesNotExist:
            pass
    return render(request, 'basket.html', {'items': items, 'item_total': total_count, 'order_id': order_id})


@login_required
def checkout(request, order_id):
    return render(request, 'checkout.html', None)


def basket_default(request):
    pk_x = -1
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(customer_id=request.user, placed=False)
            pk_x = order.pk_x
        except Order.DoesNotExist:
            pass

    return basket(request, pk_x)
    pass


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
        try:
            order = Order.objects.get(customer_id=request.user, pk_x=order_id)
            try:
                cartitems = CartItem.objects.filter(order_id=order)

                for cartitem in cartitems:
                    try:

                        product = Product.objects.get(slug=cartitem.product_id)
                        total += float(product.price) * float(cartitem.quantity)

                    except CartItem.DoesNotExist:
                        print("hi")
                        pass

            except CartItem.DoesNotExist:
                pass

        except Order.DoesNotExist:
            pass

    return HttpResponse(round(total, 2), content_type="text/plain")


def basket_total_default(request):
    order_id = -1
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(customer_id=request.user, placed=False)
            order_id = order.pk_x
        except Order.DoesNotExist:
            pass

    return basket_total(request, order_id)
