from django.urls import path
from .views import cake_list_page, custom_login
from .views import register
from . import views

urlpatterns = [
path('', views.home, name='home'),
path('login/', custom_login, name='login'),
path('cakes/', cake_list_page, name='cake-list-page'),
path('register/', register, name='register'),
]
