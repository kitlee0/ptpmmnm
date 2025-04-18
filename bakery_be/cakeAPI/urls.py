from django.urls import path
from .views import CakeListView, CakeDetailView,CategoryListView, CategoryDetailView, home # Import view

urlpatterns = [
    path('', home, name='home'),
    path('cakes/', CakeListView.as_view(), name='cake-list'),
    path('cakes/<str:pk>/', CakeDetailView.as_view(), name='cake-detail'), # GET, PUT, DELETE
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<str:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]