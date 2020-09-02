from django.urls import path

from shop import views

urlpatterns = [
    path('products/list', views.product_list, name='product_list'), 
    path('products/basket/', views.basket_default, name='basket-default'),  
    path('products/basket/<str:order_id>', views.basket, name='basket'),  
    path('add-basket/<str:product_id>', views.add_basket),  
    path('remove-basket/<str:product_id>', views.remove_basket),  
    path('basket-total/', views.basket_total_default),  
    path('basket-total/<str:order_id>', views.basket_total),  
    path('checkout/<str:order_id>', views.checkout, name='checkout')
]
