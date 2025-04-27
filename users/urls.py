from django.urls import path
from .views import create_user
from . import views

urlpatterns = [
    path('create-user/', create_user, name='create_user'),
    path('login-user/', views.login_user, name='login_user'),
]
