from django.contrib import admin

from shop.models import Address, CartItem, Order, Payment

admin.site.register(Payment)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(CartItem)
