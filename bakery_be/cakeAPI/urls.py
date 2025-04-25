from django.urls import include, path
from .views import CakeListView, CakeDetailView,CategoryListView, CategoryDetailView, OrderDetailView, OrderListView, PaymentDetailView, PaymentListView, UserDetailView, UserListView, home # Import view

urlpatterns = [
    path('', home, name='home'),
    path('cakes/', CakeListView.as_view(), name='cake-list'),
    path('cakes/<str:pk>/', CakeDetailView.as_view(), name='cake-detail'), # GET, PUT, DELETE
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<str:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<str:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/<str:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<str:pk>/', OrderDetailView.as_view(), name='order-detail'),
]