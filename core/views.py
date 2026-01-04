"""
API views для mock-объектов бизнес-приложения.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, Order, Shop
from .serializers import (
    ProductSerializer,
    ProductCreateUpdateSerializer,
    OrderSerializer,
    OrderCreateUpdateSerializer,
    ShopSerializer,
    ShopCreateUpdateSerializer
)
from access.permissions import (
    CanReadElement,
    CanCreateElement,
    CanUpdateElement,
    CanDeleteElement
)
from access.utils import check_permission
from access.exceptions import ForbiddenError


class ProductListView(APIView):
    """
    GET /api/core/products/ - список продуктов
    POST /api/core/products/ - создание продукта
    """
    permission_classes = [IsAuthenticated, CanReadElement, CanCreateElement]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element_name = 'products'

    def get(self, request):
        """Возвращает список продуктов с учетом прав доступа."""
        # Получаем правило доступа для проверки read_all_permission
        from access.models import AccessRule, BusinessElement
        try:
            element = BusinessElement.objects.get(name='products')
            access_rule = AccessRule.objects.get(
                role=request.user.role,
                element=element
            )
            # Если есть read_all_permission, показываем все продукты
            if access_rule.read_all_permission:
                products = Product.objects.select_related('owner').all()
            # Если есть read_permission, показываем только свои
            elif access_rule.read_permission:
                products = Product.objects.select_related('owner').filter(owner=request.user)
            else:
                raise ForbiddenError('У вас нет прав на чтение продуктов.')
        except (AccessRule.DoesNotExist, BusinessElement.DoesNotExist):
            raise ForbiddenError('У вас нет прав на чтение продуктов.')

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Создает новый продукт."""
        serializer = ProductCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            # Устанавливаем владельца продукта
            product = serializer.save(owner=request.user)
            # Возвращаем через ProductSerializer
            response_serializer = ProductSerializer(product)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductDetailView(APIView):
    """
    GET /api/core/products/{id}/ - детали продукта
    PUT/PATCH /api/core/products/{id}/ - обновление продукта
    DELETE /api/core/products/{id}/ - удаление продукта
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element_name = 'products'

    def get(self, request, pk):
        """Возвращает детали продукта."""
        try:
            product = Product.objects.select_related('owner').get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'Продукт не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем право на чтение
        has_read = check_permission(
            user=request.user,
            element_name='products',
            action='read',
            resource_owner=product.owner
        )

        if not has_read:
            raise ForbiddenError('У вас нет прав на чтение этого продукта.')

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Полное обновление продукта."""
        try:
            product = Product.objects.select_related('owner').get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'Продукт не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем право на обновление
        has_update = check_permission(
            user=request.user,
            element_name='products',
            action='update',
            resource_owner=product.owner
        )

        if not has_update:
            raise ForbiddenError('У вас нет прав на обновление этого продукта.')

        serializer = ProductCreateUpdateSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_serializer = ProductSerializer(product)
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        """Частичное обновление продукта."""
        try:
            product = Product.objects.select_related('owner').get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'Продукт не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем право на обновление
        has_update = check_permission(
            user=request.user,
            element_name='products',
            action='update',
            resource_owner=product.owner
        )

        if not has_update:
            raise ForbiddenError('У вас нет прав на обновление этого продукта.')

        serializer = ProductCreateUpdateSerializer(
            product,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            response_serializer = ProductSerializer(product)
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        """Удаление продукта."""
        try:
            product = Product.objects.select_related('owner').get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'Продукт не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем право на удаление
        has_delete = check_permission(
            user=request.user,
            element_name='products',
            action='delete',
            resource_owner=product.owner
        )

        if not has_delete:
            raise ForbiddenError('У вас нет прав на удаление этого продукта.')

        product.delete()
        return Response(
            {'message': 'Продукт успешно удален.'},
            status=status.HTTP_200_OK
        )


class OrderListView(APIView):
    """
    GET /api/core/orders/ - список заказов
    POST /api/core/orders/ - создание заказа
    """
    permission_classes = [IsAuthenticated, CanReadElement, CanCreateElement]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element_name = 'orders'

    def get(self, request):
        """Возвращает список заказов с учетом прав доступа."""
        # Получаем правило доступа для проверки read_all_permission
        from access.models import AccessRule, BusinessElement
        try:
            element = BusinessElement.objects.get(name='orders')
            access_rule = AccessRule.objects.get(
                role=request.user.role,
                element=element
            )
            # Если есть read_all_permission, показываем все заказы
            if access_rule.read_all_permission:
                orders = Order.objects.select_related('owner', 'product').all()
            # Если есть read_permission, показываем только свои
            elif access_rule.read_permission:
                orders = Order.objects.select_related('owner', 'product').filter(owner=request.user)
            else:
                raise ForbiddenError('У вас нет прав на чтение заказов.')
        except (AccessRule.DoesNotExist, BusinessElement.DoesNotExist):
            raise ForbiddenError('У вас нет прав на чтение заказов.')

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Создает новый заказ."""
        serializer = OrderCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            # Устанавливаем владельца заказа
            order = serializer.save(owner=request.user)
            # Возвращаем через OrderSerializer
            response_serializer = OrderSerializer(order)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderDetailView(APIView):
    """
    GET /api/core/orders/{id}/ - детали заказа
    PUT/PATCH /api/core/orders/{id}/ - обновление заказа
    DELETE /api/core/orders/{id}/ - удаление заказа
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element_name = 'orders'

    def get(self, request, pk):
        """Возвращает детали заказа."""
        try:
            order = Order.objects.select_related('owner', 'product').get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {'detail': 'Заказ не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем право на чтение
        has_read = check_permission(
            user=request.user,
            element_name='orders',
            action='read',
            resource_owner=order.owner
        )

        if not has_read:
            raise ForbiddenError('У вас нет прав на чтение этого заказа.')

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Полное обновление заказа."""
        try:
            order = Order.objects.select_related('owner', 'product').get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {'detail': 'Заказ не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем право на обновление
        has_update = check_permission(
            user=request.user,
            element_name='orders',
            action='update',
            resource_owner=order.owner
        )

        if not has_update:
            raise ForbiddenError('У вас нет прав на обновление этого заказа.')

        serializer = OrderCreateUpdateSerializer(order, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_serializer = OrderSerializer(order)
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        """Частичное обновление заказа."""
        try:
            order = Order.objects.select_related('owner', 'product').get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {'detail': 'Заказ не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем право на обновление
        has_update = check_permission(
            user=request.user,
            element_name='orders',
            action='update',
            resource_owner=order.owner
        )

        if not has_update:
            raise ForbiddenError('У вас нет прав на обновление этого заказа.')

        serializer = OrderCreateUpdateSerializer(
            order,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            response_serializer = OrderSerializer(order)
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        """Удаление заказа."""
        try:
            order = Order.objects.select_related('owner', 'product').get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {'detail': 'Заказ не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем право на удаление
        has_delete = check_permission(
            user=request.user,
            element_name='orders',
            action='delete',
            resource_owner=order.owner
        )

        if not has_delete:
            raise ForbiddenError('У вас нет прав на удаление этого заказа.')

        order.delete()
        return Response(
            {'message': 'Заказ успешно удален.'},
            status=status.HTTP_200_OK
        )


class ShopListView(APIView):
    """
    GET /api/core/shops/ - список магазинов
    POST /api/core/shops/ - создание магазина
    """
    permission_classes = [IsAuthenticated, CanReadElement, CanCreateElement]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element_name = 'shops'

    def get(self, request):
        """Возвращает список магазинов с учетом прав доступа."""
        # Получаем правило доступа для проверки read_all_permission
        from access.models import AccessRule, BusinessElement
        try:
            element = BusinessElement.objects.get(name='shops')
            access_rule = AccessRule.objects.get(
                role=request.user.role,
                element=element
            )
            # Если есть read_all_permission, показываем все магазины
            if access_rule.read_all_permission:
                shops = Shop.objects.select_related('owner').all()
            # Если есть read_permission, показываем только свои
            elif access_rule.read_permission:
                shops = Shop.objects.select_related('owner').filter(owner=request.user)
            else:
                raise ForbiddenError('У вас нет прав на чтение магазинов.')
        except (AccessRule.DoesNotExist, BusinessElement.DoesNotExist):
            raise ForbiddenError('У вас нет прав на чтение магазинов.')

        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Создает новый магазин."""
        serializer = ShopCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            # Устанавливаем владельца магазина
            shop = serializer.save(owner=request.user)
            # Возвращаем через ShopSerializer
            response_serializer = ShopSerializer(shop)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ShopDetailView(APIView):
    """
    GET /api/core/shops/{id}/ - детали магазина
    PUT/PATCH /api/core/shops/{id}/ - обновление магазина
    DELETE /api/core/shops/{id}/ - удаление магазина
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element_name = 'shops'

    def get(self, request, pk):
        """Возвращает детали магазина."""
        try:
            shop = Shop.objects.select_related('owner').get(pk=pk)
        except Shop.DoesNotExist:
            return Response(
                {'detail': 'Магазин не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем право на чтение
        has_read = check_permission(
            user=request.user,
            element_name='shops',
            action='read',
            resource_owner=shop.owner
        )

        if not has_read:
            raise ForbiddenError('У вас нет прав на чтение этого магазина.')

        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Полное обновление магазина."""
        try:
            shop = Shop.objects.select_related('owner').get(pk=pk)
        except Shop.DoesNotExist:
            return Response(
                {'detail': 'Магазин не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем право на обновление
        has_update = check_permission(
            user=request.user,
            element_name='shops',
            action='update',
            resource_owner=shop.owner
        )

        if not has_update:
            raise ForbiddenError('У вас нет прав на обновление этого магазина.')

        serializer = ShopCreateUpdateSerializer(shop, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_serializer = ShopSerializer(shop)
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        """Частичное обновление магазина."""
        try:
            shop = Shop.objects.select_related('owner').get(pk=pk)
        except Shop.DoesNotExist:
            return Response(
                {'detail': 'Магазин не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем право на обновление
        has_update = check_permission(
            user=request.user,
            element_name='shops',
            action='update',
            resource_owner=shop.owner
        )

        if not has_update:
            raise ForbiddenError('У вас нет прав на обновление этого магазина.')

        serializer = ShopCreateUpdateSerializer(
            shop,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            response_serializer = ShopSerializer(shop)
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        """Удаление магазина."""
        try:
            shop = Shop.objects.select_related('owner').get(pk=pk)
        except Shop.DoesNotExist:
            return Response(
                {'detail': 'Магазин не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем право на удаление
        has_delete = check_permission(
            user=request.user,
            element_name='shops',
            action='delete',
            resource_owner=shop.owner
        )

        if not has_delete:
            raise ForbiddenError('У вас нет прав на удаление этого магазина.')

        shop.delete()
        return Response(
            {'message': 'Магазин успешно удален.'},
            status=status.HTTP_200_OK
        )
