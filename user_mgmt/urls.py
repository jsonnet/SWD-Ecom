from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index2'),
    path('login/', auth_views.LoginView.as_view(template_name='user_mgmt/login.html'), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('registration/', views.register, name='registration'),
    path('<str:email>/verify/<str:token>', views.verify_user, name='verify'),
    path('sso-login', views.sso_verify_login, name='sso-login'),
    path('password-reset', views.reset_pw_req, name='reset-pw-req'),
    path('<str:username>/pw-reset/<str:token>', views.reset_pw, name='reset-pw')
]
