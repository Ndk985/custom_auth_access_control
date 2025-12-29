from django.db import models


class Role(models.Model):
    """
    Модель ролей пользователей в системе.
    
    Предустановленные роли:
    - admin: Администратор системы с полным доступом
    - manager: Менеджер с расширенными правами
    - user: Обычный пользователь с базовыми правами
    - guest: Гость с минимальными правами
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name='Название роли',
        help_text='Уникальное название роли (например: admin, manager, user)'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Описание роли и её назначения в системе'
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
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        ordering = ['name']
        db_table = 'access_role'

    def __str__(self):
        return self.name


class BusinessElement(models.Model):
    """
    Модель бизнес-элементов (ресурсов) системы.
    
    Описывает ресурсы, к которым применяются правила доступа.
    Предустановленные элементы:
    - users: Управление пользователями
    - products: Управление товарами
    - orders: Управление заказами
    - shops: Управление магазинами
    - access_rules: Управление правилами доступа
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name='Название элемента',
        help_text=(
            'Уникальное название бизнес-элемента '
            '(например: users, products, orders)'
        )
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Описание элемента и его назначения в системе'
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
        verbose_name = 'Бизнес-элемент'
        verbose_name_plural = 'Бизнес-элементы'
        ordering = ['name']
        db_table = 'access_businesselement'

    def __str__(self):
        return self.name


class AccessRule(models.Model):
    """
    Модель правил доступа ролей к бизнес-элементам.
    
    Определяет, какие действия может совершать роль с ресурсом:
    - read_permission: чтение собственных ресурсов
    - read_all_permission: чтение всех ресурсов
    - create_permission: создание ресурсов
    - update_permission: обновление собственных ресурсов
    - update_all_permission: обновление всех ресурсов
    - delete_permission: удаление собственных ресурсов
    - delete_all_permission: удаление всех ресурсов
    
    Логика приоритета:
    - Если *_all_permission = True → доступ ко всем ресурсам
    - Если *_permission = True → доступ только к ресурсам, где owner = user
    - Если оба False → доступ запрещен
    """
    role = models.ForeignKey(
        'Role',
        on_delete=models.CASCADE,
        related_name='access_rules',
        db_index=True,
        verbose_name='Роль',
        help_text='Роль, для которой применяется правило'
    )
    element = models.ForeignKey(
        'BusinessElement',
        on_delete=models.CASCADE,
        related_name='access_rules',
        db_index=True,
        verbose_name='Бизнес-элемент',
        help_text='Элемент, к которому применяется правило'
    )
    read_permission = models.BooleanField(
        default=False,
        verbose_name='Чтение своих',
        help_text='Разрешение на чтение собственных ресурсов'
    )
    read_all_permission = models.BooleanField(
        default=False,
        verbose_name='Чтение всех',
        help_text='Разрешение на чтение всех ресурсов'
    )
    create_permission = models.BooleanField(
        default=False,
        verbose_name='Создание',
        help_text='Разрешение на создание ресурсов'
    )
    update_permission = models.BooleanField(
        default=False,
        verbose_name='Обновление своих',
        help_text='Разрешение на обновление собственных ресурсов'
    )
    update_all_permission = models.BooleanField(
        default=False,
        verbose_name='Обновление всех',
        help_text='Разрешение на обновление всех ресурсов'
    )
    delete_permission = models.BooleanField(
        default=False,
        verbose_name='Удаление своих',
        help_text='Разрешение на удаление собственных ресурсов'
    )
    delete_all_permission = models.BooleanField(
        default=False,
        verbose_name='Удаление всех',
        help_text='Разрешение на удаление всех ресурсов'
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
        verbose_name = 'Правило доступа'
        verbose_name_plural = 'Правила доступа'
        ordering = ['role', 'element']
        db_table = 'access_accessrule'
        unique_together = [['role', 'element']]

    def __str__(self):
        return f'{self.role.name} → {self.element.name}'
