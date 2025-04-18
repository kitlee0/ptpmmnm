from django.urls import path
from .views import custom_login
from .views import register
from . import views

urlpatterns = [
path('', views.home, name='home'),
path('login/', custom_login, name='login'),
path('register/', register, name='register'),
]
