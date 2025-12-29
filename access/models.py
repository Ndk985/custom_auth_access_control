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
