from django.contrib import admin
from .models import Role, BusinessElement, AccessRule


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Role."""
    list_display = ('name', 'description', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)


@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели BusinessElement."""
    list_display = ('name', 'description', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)


@admin.register(AccessRule)
class AccessRuleAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели AccessRule."""
    list_display = (
        'role', 'element', 'read_permission', 'read_all_permission',
        'create_permission', 'update_permission', 'update_all_permission',
        'delete_permission', 'delete_all_permission', 'created_at'
    )
    list_filter = (
        'role', 'element', 'read_permission', 'read_all_permission',
        'create_permission', 'update_permission', 'update_all_permission',
        'delete_permission', 'delete_all_permission', 'created_at',
        'updated_at'
    )
    search_fields = ('role__name', 'element__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('role', 'element')
    fieldsets = (
        ('Основная информация', {
            'fields': ('role', 'element')
        }),
        ('Разрешения на чтение', {
            'fields': ('read_permission', 'read_all_permission')
        }),
        ('Разрешения на создание', {
            'fields': ('create_permission',)
        }),
        ('Разрешения на обновление', {
            'fields': ('update_permission', 'update_all_permission')
        }),
        ('Разрешения на удаление', {
            'fields': ('delete_permission', 'delete_all_permission')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
