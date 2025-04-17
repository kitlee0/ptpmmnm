from django.urls import path
from .views import CakeListView  # Import view

urlpatterns = [
    path('cakes/', CakeListView.as_view(), name='cake-list'),
    path('cakes/<str:pk>/', CakeListView.as_view(), name='cake-detail'),  # PUT và DELETE
]