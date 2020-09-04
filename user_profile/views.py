from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from shop.models import Address, Order
from shop_mgmt.models import Product
from user_mgmt.models import UserProfile


@login_required
def private_profile(request, email):
    if str(request.user) == email:
        # No need to catch something as a empty QuerySet is handled in template
        orders = Order.objects.filter(customer_id=request.user)

        address = Address.objects.filter(user=request.user)
        try:
            address = address.reverse()[0]  # once we have multiple addresses use the last one
        except IndexError:
            pass

        # Cannot throw error, as the user is obviously login in with this User
        profile = UserProfile.objects.get(username=email)

        return render(request, 'private_profile.html', {'orders': orders, 'address': address, 'profile': profile})

    return HttpResponse(status=401)


@xframe_options_exempt
@login_required
def public_store(request, email):

    products = Product.objects.filter(seller=f'u-{email}')

    return render(request, 'public_shop.html', {'products': products})
