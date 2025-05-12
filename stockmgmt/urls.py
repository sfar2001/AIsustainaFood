from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='stock_dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
]