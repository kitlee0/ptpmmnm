from django.urls import path
from .views import CakeListView, CakeDetailView  # Import view

urlpatterns = [
    path('cakes/', CakeListView.as_view(), name='cake-list'),
    path('cakes/<str:pk>/', CakeDetailView.as_view()) # GET, PUT, DELETE
]