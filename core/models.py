"""
Модели для mock-объектов бизнес-приложения.
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    """
    Модель продукта (товара).
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Название продукта'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Описание продукта'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
        help_text='Цена продукта'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Владелец',
        help_text='Пользователь, создавший продукт'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']
        db_table = 'core_product'

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Модель заказа.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Продукт',
        help_text='Продукт в заказе'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество',
        help_text='Количество единиц продукта'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Владелец',
        help_text='Пользователь, создавший заказ'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
        db_table = 'core_order'

    def __str__(self):
        return f'Заказ #{self.id} - {self.product.name} x{self.quantity}'


class Shop(models.Model):
    """
    Модель магазина.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Название магазина'
    )
    address = models.CharField(
        max_length=500,
        verbose_name='Адрес',
        help_text='Адрес магазина'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shops',
        verbose_name='Владелец',
        help_text='Пользователь, создавший магазин'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['-created_at']
        db_table = 'core_shop'

    def __str__(self):
        return self.name
