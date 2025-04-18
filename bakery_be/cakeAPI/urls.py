from django.urls import path
from .views import CakeListView, CakeDetailView,CategoryListView, CategoryDetailView, PaymentDetailView, PaymentListView, UserDetailView, UserListView # Import view

urlpatterns = [
    path('cakes/', CakeListView.as_view(), name='cake-list'),
    path('cakes/<str:pk>/', CakeDetailView.as_view(), name='cake-detail'), # GET, PUT, DELETE
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<str:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<str:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/<str:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
]