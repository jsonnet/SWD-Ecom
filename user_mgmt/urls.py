from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('login', views.login_view, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='user_mgmt/login.html'), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('registration', views.register, name='registration')
]
