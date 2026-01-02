"""
Утилиты для проверки прав доступа к ресурсам.
"""
from typing import Optional
from .models import AccessRule, BusinessElement
from django.contrib.auth import get_user_model

User = get_user_model()


def check_permission(
    user,
    element_name: str,
    action: str,
    resource_owner: Optional[User] = None
) -> bool:
    """
    Проверяет, имеет ли пользователь право на выполнение действия с ресурсом.

    Args:
        user: Объект пользователя
        element_name: Название бизнес-элемента (например: 'products', 'orders')
        action: Действие для проверки ('read', 'create', 'update', 'delete')
        resource_owner: Владелец ресурса (для проверки "своих" разрешений).
                       Если None, проверяется только право на действие.

    Returns:
        bool: True если доступ разрешен, False в противном случае

    Raises:
        ValueError: Если action не поддерживается
    """
    # Проверяем, что пользователь активен
    if not user or not user.is_active:
        return False

    # Суперпользователь имеет все права
    if user.is_superuser:
        return True

    # Получаем роль пользователя
    if not hasattr(user, 'role') or not user.role:
        return False

    # Получаем бизнес-элемент
    try:
        element = BusinessElement.objects.get(name=element_name)
    except BusinessElement.DoesNotExist:
        return False

    # Получаем правило доступа для роли и элемента
    try:
        access_rule = AccessRule.objects.get(
            role=user.role,
            element=element
        )
    except AccessRule.DoesNotExist:
        # Если правило не найдено, доступ запрещен
        return False

    # Проверяем конкретное действие
    if action == 'read':
        # Для чтения: если read_all_permission = True, доступ ко всем
        # Если read_permission = True, доступ только к своим
        if access_rule.read_all_permission:
            return True
        if access_rule.read_permission:
            # Проверяем, что ресурс принадлежит пользователю
            if resource_owner is not None:
                return resource_owner == user
            # Если resource_owner не указан, считаем что доступ есть
            # (будет проверено в конкретном view)
            return True
        return False

    elif action == 'create':
        # Для создания достаточно create_permission
        return access_rule.create_permission

    elif action == 'update':
        # Для обновления: если update_all_permission = True, доступ ко всем
        # Если update_permission = True, доступ только к своим
        if access_rule.update_all_permission:
            return True
        if access_rule.update_permission:
            # Проверяем, что ресурс принадлежит пользователю
            if resource_owner is not None:
                return resource_owner == user
            # Если resource_owner не указан, считаем что доступ есть
            return True
        return False

    elif action == 'delete':
        # Для удаления: если delete_all_permission = True, доступ ко всем
        # Если delete_permission = True, доступ только к своим
        if access_rule.delete_all_permission:
            return True
        if access_rule.delete_permission:
            # Проверяем, что ресурс принадлежит пользователю
            if resource_owner is not None:
                return resource_owner == user
            # Если resource_owner не указан, считаем что доступ есть
            return True
        return False

    else:
        raise ValueError(f'Неподдерживаемое действие: {action}')

