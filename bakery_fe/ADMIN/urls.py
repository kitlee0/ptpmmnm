from django.urls import path
from . import views

urlpatterns = [
    path('cakes/', views.admin_cakes_view, name='admin_cakes'),
    
    path('cakes/add/', views.admin_add_cake, name='admin_add_cake'),  # Đảm bảo thêm đúng đường dẫn
    path('cakes/edit/<str:cake_id>/', views.admin_edit_cake, name='admin_edit_cake'),
    path('cakes/delete/<str:cake_id>/', views.admin_delete_cake, name='admin_delete_cake'),
]
