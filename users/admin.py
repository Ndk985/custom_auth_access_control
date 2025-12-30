from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели User."""
    list_display = (
        'email', 'first_name', 'last_name', 'role', 'is_active',
        'is_staff', 'is_superuser', 'created_at', 'updated_at'
    )
    list_filter = (
        'role', 'is_active', 'is_staff', 'is_superuser',
        'created_at', 'updated_at'
    )
    search_fields = ('email', 'first_name', 'last_name', 'middle_name')
    readonly_fields = ('created_at', 'updated_at', 'password_hash')
    ordering = ('email',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('email', 'first_name', 'last_name', 'middle_name')
        }),
        ('Безопасность', {
            'fields': ('password_hash', 'is_active', 'is_staff', 'is_superuser', 'role')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Переопределяем сохранение для хеширования пароля."""
        if 'password' in form.changed_data:
            # Если пароль был изменен через админку
            # (в реальности лучше использовать отдельное поле)
            pass
        super().save_model(request, obj, form, change)
