"""
Сериализаторы для работы с правилами доступа.
"""
from rest_framework import serializers
from .models import AccessRule, Role, BusinessElement


class AccessRuleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения правил доступа.
    """
    role_name = serializers.CharField(
        source='role.name',
        read_only=True
    )
    element_name = serializers.CharField(
        source='element.name',
        read_only=True
    )

    class Meta:
        model = AccessRule
        fields = (
            'id',
            'role',
            'role_name',
            'element',
            'element_name',
            'read_permission',
            'read_all_permission',
            'create_permission',
            'update_permission',
            'update_all_permission',
            'delete_permission',
            'delete_all_permission',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class AccessRuleCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления правил доступа.
    """
    class Meta:
        model = AccessRule
        fields = (
            'id',
            'role',
            'element',
            'read_permission',
            'read_all_permission',
            'create_permission',
            'update_permission',
            'update_all_permission',
            'delete_permission',
            'delete_all_permission'
        )
        read_only_fields = ('id',)

    def validate(self, attrs):
        """
        Валидация данных правила доступа.
        """
        role = attrs.get('role')
        element = attrs.get('element')

        # Проверяем, что роль и элемент указаны
        if not role:
            raise serializers.ValidationError({
                'role': 'Роль обязательна для заполнения.'
            })
        if not element:
            raise serializers.ValidationError({
                'element': 'Бизнес-элемент обязателен для заполнения.'
            })

        # Проверяем уникальность пары (role, element)
        # Если это обновление существующего объекта, исключаем его из проверки
        instance = self.instance
        if instance:
            existing_rule = AccessRule.objects.filter(
                role=role,
                element=element
            ).exclude(pk=instance.pk).first()
        else:
            existing_rule = AccessRule.objects.filter(
                role=role,
                element=element
            ).first()

        if existing_rule:
            raise serializers.ValidationError({
                'non_field_errors': [
                    f'Правило доступа для роли "{role.name}" '
                    f'и элемента "{element.name}" уже существует.'
                ]
            })

        return attrs

