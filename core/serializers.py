"""
Сериализаторы для mock-объектов бизнес-приложения.
"""
from rest_framework import serializers
from .models import Product, Order, Shop
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продукта."""
    owner_email = serializers.CharField(
        source='owner.email',
        read_only=True
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'owner',
            'owner_email',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner_email')


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления продукта."""

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price'
        )
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заказа."""
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )
    owner_email = serializers.CharField(
        source='owner.email',
        read_only=True
    )

    class Meta:
        model = Order
        fields = (
            'id',
            'product',
            'product_name',
            'quantity',
            'owner',
            'owner_email',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner_email', 'product_name')


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления заказа."""

    class Meta:
        model = Order
        fields = (
            'id',
            'product',
            'quantity'
        )
        read_only_fields = ('id',)


class ShopSerializer(serializers.ModelSerializer):
    """Сериализатор для магазина."""
    owner_email = serializers.CharField(
        source='owner.email',
        read_only=True
    )

    class Meta:
        model = Shop
        fields = (
            'id',
            'name',
            'address',
            'owner',
            'owner_email',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner_email')


class ShopCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления магазина."""

    class Meta:
        model = Shop
        fields = (
            'id',
            'name',
            'address'
        )
        read_only_fields = ('id',)

