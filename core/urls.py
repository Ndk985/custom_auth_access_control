"""
URL маршруты для приложения core.
"""
from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    OrderListView,
    OrderDetailView,
    ShopListView,
    ShopDetailView
)

app_name = 'core'

urlpatterns = [
    # Products
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    # Orders
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    # Shops
    path('shops/', ShopListView.as_view(), name='shop-list'),
    path('shops/<int:pk>/', ShopDetailView.as_view(), name='shop-detail'),
]

