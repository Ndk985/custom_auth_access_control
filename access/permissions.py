"""
Permission classes для проверки прав доступа к ресурсам.
"""
from rest_framework import permissions
from .utils import check_permission
from .exceptions import UnauthorizedError, ForbiddenError


class HasElementPermission(permissions.BasePermission):
    """
    Базовый permission class для проверки прав доступа к бизнес-элементу.

    Используется как базовый класс для специализированных permission classes.
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь право на доступ к ресурсу.

        Args:
            request: HTTP запрос
            view: View, для которого проверяется доступ

        Returns:
            bool: True если доступ разрешен, False в противном случае
        """
        # Проверяем аутентификацию
        if not request.user or not request.user.is_authenticated:
            raise UnauthorizedError()

        # Получаем название элемента из view
        element_name = getattr(view, 'element_name', None)
        if not element_name:
            # Если element_name не указан, доступ запрещен
            raise ForbiddenError('Не указан элемент для проверки доступа.')

        # Получаем действие из view
        action = getattr(view, 'permission_action', None)
        if not action:
            # Если action не указан, пытаемся определить из метода запроса
            action = self._get_action_from_method(request.method)

        # Проверяем право доступа
        has_access = check_permission(
            user=request.user,
            element_name=element_name,
            action=action
        )

        if not has_access:
            raise ForbiddenError(
                f'У вас нет прав на выполнение действия "{action}" '
                f'с элементом "{element_name}".'
            )

        return True

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, имеет ли пользователь право на доступ к конкретному объекту.

        Args:
            request: HTTP запрос
            view: View, для которого проверяется доступ
            obj: Объект, к которому проверяется доступ

        Returns:
            bool: True если доступ разрешен, False в противном случае
        """
        # Сначала проверяем базовое разрешение
        if not self.has_permission(request, view):
            return False

        # Получаем владельца ресурса
        resource_owner = getattr(obj, 'owner', None)

        # Получаем название элемента и действие
        element_name = getattr(view, 'element_name', None)
        action = getattr(view, 'permission_action', None)
        if not action:
            action = self._get_action_from_method(request.method)

        # Проверяем право доступа с учетом владельца
        has_access = check_permission(
            user=request.user,
            element_name=element_name,
            action=action,
            resource_owner=resource_owner
        )

        if not has_access:
            raise ForbiddenError(
                f'У вас нет прав на выполнение действия "{action}" '
                f'с этим ресурсом.'
            )

        return True

    def _get_action_from_method(self, method: str) -> str:
        """
        Определяет действие из HTTP метода.

        Args:
            method: HTTP метод (GET, POST, PUT, PATCH, DELETE)

        Returns:
            str: Название действия ('read', 'create', 'update', 'delete')
        """
        method_to_action = {
            'GET': 'read',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete',
        }
        return method_to_action.get(method.upper(), 'read')


class CanReadElement(HasElementPermission):
    """Permission class для проверки права на чтение ресурса."""

    def has_permission(self, request, view):
        """Проверяет право на чтение."""
        if not request.user or not request.user.is_authenticated:
            raise UnauthorizedError()

        element_name = getattr(view, 'element_name', None)
        if not element_name:
            raise ForbiddenError('Не указан элемент для проверки доступа.')

        has_access = check_permission(
            user=request.user,
            element_name=element_name,
            action='read'
        )

        if not has_access:
            raise ForbiddenError(
                f'У вас нет прав на чтение элемента "{element_name}".'
            )

        return True


class CanCreateElement(HasElementPermission):
    """Permission class для проверки права на создание ресурса."""

    def has_permission(self, request, view):
        """Проверяет право на создание."""
        if not request.user or not request.user.is_authenticated:
            raise UnauthorizedError()

        element_name = getattr(view, 'element_name', None)
        if not element_name:
            raise ForbiddenError('Не указан элемент для проверки доступа.')

        has_access = check_permission(
            user=request.user,
            element_name=element_name,
            action='create'
        )

        if not has_access:
            raise ForbiddenError(
                f'У вас нет прав на создание элемента "{element_name}".'
            )

        return True


class CanUpdateElement(HasElementPermission):
    """Permission class для проверки права на обновление ресурса."""

    def has_object_permission(self, request, view, obj):
        """Проверяет право на обновление конкретного объекта."""
        if not request.user or not request.user.is_authenticated:
            raise UnauthorizedError()

        element_name = getattr(view, 'element_name', None)
        if not element_name:
            raise ForbiddenError('Не указан элемент для проверки доступа.')

        resource_owner = getattr(obj, 'owner', None)

        has_access = check_permission(
            user=request.user,
            element_name=element_name,
            action='update',
            resource_owner=resource_owner
        )

        if not has_access:
            raise ForbiddenError(
                f'У вас нет прав на обновление этого ресурса.'
            )

        return True


class CanDeleteElement(HasElementPermission):
    """Permission class для проверки права на удаление ресурса."""

    def has_object_permission(self, request, view, obj):
        """Проверяет право на удаление конкретного объекта."""
        if not request.user or not request.user.is_authenticated:
            raise UnauthorizedError()

        element_name = getattr(view, 'element_name', None)
        if not element_name:
            raise ForbiddenError('Не указан элемент для проверки доступа.')

        resource_owner = getattr(obj, 'owner', None)

        has_access = check_permission(
            user=request.user,
            element_name=element_name,
            action='delete',
            resource_owner=resource_owner
        )

        if not has_access:
            raise ForbiddenError(
                f'У вас нет прав на удаление этого ресурса.'
            )

        return True

