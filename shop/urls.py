from django.urls import path

from shop import views

urlpatterns = [
    path('products/list', views.product_list, name='product_list'), 
    path('products/basket/<str:order_id>', views.basket, name='basket'),
    path('checkout/<str:order_id>', views.checkout, name='checkout')
]
