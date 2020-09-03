from django.conf.urls import url
from django.urls import include, path

from . import views

urlpatterns = [
    path('<str:email>/private', views.private_profile, name='private_profile'),
    path('<str:email>/public-store', views.public_store, name='public_store')
]
