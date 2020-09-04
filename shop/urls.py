from django.urls import path

from shop import views

urlpatterns = [
    path('products/list', views.product_list, name='product_list'),
    path('products/basket/', views.basket_default, name='basket-default'),
    path('products/basket/<str:order_id>', views.basket, name='basket'),
    path('checkout/<str:order_id>', views.checkout, name='checkout'),

    # CDN
    path('add-basket/<str:product_id>', views.add_basket),  # returns login[-required] or redirect
    path('remove-basket/<str:product_id>', views.remove_basket),  # returns error or done
    path('basket-total/', views.basket_total_default),  # returns plain total
]
