"""
API views для работы с правилами доступа.
"""
import logging
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger('access.views')
from .models import AccessRule, Role, BusinessElement
from .serializers import (
    AccessRuleSerializer,
    AccessRuleCreateUpdateSerializer,
    RoleSerializer,
    RoleCreateUpdateSerializer,
    BusinessElementSerializer,
    BusinessElementCreateUpdateSerializer
)
from .permissions import IsAdminRole


class AccessRuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления правилами доступа.

    Доступ разрешен только пользователям с ролью 'admin'.
    """
    queryset = AccessRule.objects.select_related('role', 'element').all()
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора в зависимости от действия.
        """
        if self.action in ('create', 'update', 'partial_update'):
            return AccessRuleCreateUpdateSerializer
        return AccessRuleSerializer

    def list(self, request):
        """
        GET /api/access/rules/
        Возвращает список всех правил доступа.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        GET /api/access/rules/{id}/
        Возвращает детали конкретного правила доступа.
        """
        try:
            access_rule = self.get_object()
            serializer = self.get_serializer(access_rule)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccessRule.DoesNotExist:
            return Response(
                {'detail': 'Правило доступа не найдено.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        """
        POST /api/access/rules/
        Создает новое правило доступа.
        """
        serializer = AccessRuleCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            access_rule = serializer.save()
            # Возвращаем созданное правило через AccessRuleSerializer
            response_serializer = AccessRuleSerializer(access_rule)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):
        """
        PUT /api/access/rules/{id}/
        Полное обновление правила доступа.
        """
        try:
            access_rule = self.get_object()
            serializer = AccessRuleCreateUpdateSerializer(
                access_rule,
                data=request.data
            )

            if serializer.is_valid():
                serializer.save()
                logger.info(
                    f'Обновлено правило доступа ID {access_rule.id}: '
                    f'роль {access_rule.role.name}, элемент {access_rule.element.name}, '
                    f'пользователь {request.user.email}'
                )
                # Возвращаем обновленное правило через AccessRuleSerializer
                response_serializer = AccessRuleSerializer(access_rule)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except AccessRule.DoesNotExist:
            return Response(
                {'detail': 'Правило доступа не найдено.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request, pk=None):
        """
        PATCH /api/access/rules/{id}/
        Частичное обновление правила доступа.
        """
        try:
            access_rule = self.get_object()
            serializer = AccessRuleCreateUpdateSerializer(
                access_rule,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()
                logger.info(
                    f'Обновлено правило доступа ID {access_rule.id}: '
                    f'роль {access_rule.role.name}, элемент {access_rule.element.name}, '
                    f'пользователь {request.user.email}'
                )
                # Возвращаем обновленное правило через AccessRuleSerializer
                response_serializer = AccessRuleSerializer(access_rule)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except AccessRule.DoesNotExist:
            return Response(
                {'detail': 'Правило доступа не найдено.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        """
        DELETE /api/access/rules/{id}/
        Удаляет правило доступа.
        """
        try:
            access_rule = self.get_object()
            rule_id = access_rule.id
            role_name = access_rule.role.name
            element_name = access_rule.element.name
            access_rule.delete()
            logger.info(
                f'Удалено правило доступа ID {rule_id}: '
                f'роль {role_name}, элемент {element_name}, '
                f'пользователь {request.user.email}'
            )
            return Response(
                {'message': 'Правило доступа успешно удалено.'},
                status=status.HTTP_200_OK
            )
        except AccessRule.DoesNotExist:
            return Response(
                {'detail': 'Правило доступа не найдено.'},
                status=status.HTTP_404_NOT_FOUND
            )


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления ролями.

    Доступ разрешен только пользователям с ролью 'admin'.
    """
    queryset = Role.objects.prefetch_related('users').all()
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора в зависимости от действия.
        """
        if self.action in ('create', 'update', 'partial_update'):
            return RoleCreateUpdateSerializer
        return RoleSerializer

    def list(self, request):
        """
        GET /api/access/roles/
        Возвращает список всех ролей.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        GET /api/access/roles/{id}/
        Возвращает детали конкретной роли.
        """
        try:
            role = self.get_object()
            serializer = self.get_serializer(role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            return Response(
                {'detail': 'Роль не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        """
        POST /api/access/roles/
        Создает новую роль.
        """
        serializer = RoleCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            role = serializer.save()
            logger.info(
                f'Создана роль: {role.name}, пользователь {request.user.email}'
            )
            # Возвращаем созданную роль через RoleSerializer
            response_serializer = RoleSerializer(role)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):
        """
        PUT /api/access/roles/{id}/
        Полное обновление роли.
        """
        try:
            role = self.get_object()
            serializer = RoleCreateUpdateSerializer(
                role,
                data=request.data
            )

            if serializer.is_valid():
                serializer.save()
                logger.info(
                    f'Обновлена роль ID {role.id}: {role.name}, '
                    f'пользователь {request.user.email}'
                )
                # Возвращаем обновленную роль через RoleSerializer
                response_serializer = RoleSerializer(role)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Role.DoesNotExist:
            return Response(
                {'detail': 'Роль не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request, pk=None):
        """
        PATCH /api/access/roles/{id}/
        Частичное обновление роли.
        """
        try:
            role = self.get_object()
            serializer = RoleCreateUpdateSerializer(
                role,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()
                logger.info(
                    f'Обновлена роль ID {role.id}: {role.name}, '
                    f'пользователь {request.user.email}'
                )
                # Возвращаем обновленную роль через RoleSerializer
                response_serializer = RoleSerializer(role)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Role.DoesNotExist:
            return Response(
                {'detail': 'Роль не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        """
        DELETE /api/access/roles/{id}/
        Удаляет роль.

        Примечание: Роль нельзя удалить, если есть пользователи с этой ролью
        (защита через PROTECT в модели User).
        """
        try:
            role = self.get_object()
            # Проверяем, есть ли пользователи с этой ролью
            users_count = role.users.count()
            if users_count > 0:
                return Response(
                    {
                        'detail': (
                            f'Невозможно удалить роль. '
                            f'Существует {users_count} пользователь(ей) '
                            f'с этой ролью.'
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            role_name = role.name
            role.delete()
            logger.info(
                f'Удалена роль: {role_name}, пользователь {request.user.email}'
            )
            return Response(
                {'message': 'Роль успешно удалена.'},
                status=status.HTTP_200_OK
            )
        except Role.DoesNotExist:
            return Response(
                {'detail': 'Роль не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )


class BusinessElementViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления бизнес-элементами.

    Доступ разрешен только пользователям с ролью 'admin'.
    """
    queryset = BusinessElement.objects.prefetch_related('access_rules').all()
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора в зависимости от действия.
        """
        if self.action in ('create', 'update', 'partial_update'):
            return BusinessElementCreateUpdateSerializer
        return BusinessElementSerializer

    def list(self, request):
        """
        GET /api/access/elements/
        Возвращает список всех бизнес-элементов.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        GET /api/access/elements/{id}/
        Возвращает детали конкретного бизнес-элемента.
        """
        try:
            element = self.get_object()
            serializer = self.get_serializer(element)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BusinessElement.DoesNotExist:
            return Response(
                {'detail': 'Бизнес-элемент не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        """
        POST /api/access/elements/
        Создает новый бизнес-элемент.
        """
        serializer = BusinessElementCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            element = serializer.save()
            logger.info(
                f'Создан бизнес-элемент: {element.name}, '
                f'пользователь {request.user.email}'
            )
            # Возвращаем созданный элемент через BusinessElementSerializer
            response_serializer = BusinessElementSerializer(element)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):
        """
        PUT /api/access/elements/{id}/
        Полное обновление бизнес-элемента.
        """
        try:
            element = self.get_object()
            serializer = BusinessElementCreateUpdateSerializer(
                element,
                data=request.data
            )

            if serializer.is_valid():
                serializer.save()
                logger.info(
                    f'Обновлен бизнес-элемент ID {element.id}: {element.name}, '
                    f'пользователь {request.user.email}'
                )
                # Возвращаем обновленный элемент через BusinessElementSerializer
                response_serializer = BusinessElementSerializer(element)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except BusinessElement.DoesNotExist:
            return Response(
                {'detail': 'Бизнес-элемент не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request, pk=None):
        """
        PATCH /api/access/elements/{id}/
        Частичное обновление бизнес-элемента.
        """
        try:
            element = self.get_object()
            serializer = BusinessElementCreateUpdateSerializer(
                element,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()
                logger.info(
                    f'Обновлен бизнес-элемент ID {element.id}: {element.name}, '
                    f'пользователь {request.user.email}'
                )
                # Возвращаем обновленный элемент через BusinessElementSerializer
                response_serializer = BusinessElementSerializer(element)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except BusinessElement.DoesNotExist:
            return Response(
                {'detail': 'Бизнес-элемент не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        """
        DELETE /api/access/elements/{id}/
        Удаляет бизнес-элемент.

        Примечание: Элемент нельзя удалить, если есть правила доступа для него
        (защита через CASCADE в модели AccessRule - правила удалятся автоматически).
        """
        try:
            element = self.get_object()
            # Проверяем, есть ли правила доступа для этого элемента
            rules_count = element.access_rules.count()
            if rules_count > 0:
                return Response(
                    {
                        'detail': (
                            f'Невозможно удалить бизнес-элемент. '
                            f'Существует {rules_count} правил(а) доступа '
                            f'для этого элемента. Сначала удалите правила доступа.'
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            element_name = element.name
            element.delete()
            logger.info(
                f'Удален бизнес-элемент: {element_name}, '
                f'пользователь {request.user.email}'
            )
            return Response(
                {'message': 'Бизнес-элемент успешно удален.'},
                status=status.HTTP_200_OK
            )
        except BusinessElement.DoesNotExist:
            return Response(
                {'detail': 'Бизнес-элемент не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
