from django.urls import path

from shop_mgmt import views

urlpatterns = [
    path('test/createPartner', views.testing_partner),  # @TA For testing purposes for the following API

    path('products', views.product_list, name='product_list'),  # ?page=<int:X>&paginator=<intL:Y>; GET
    path('products/create', views.product_create),  # POST
    path('products/<str:product_id>', views.product_details)  # id = slug value; Has GET and DELETE
]
