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


class RoleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения роли.
    """
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = (
            'id',
            'name',
            'description',
            'users_count',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'users_count')

    def get_users_count(self, obj):
        """Возвращает количество пользователей с этой ролью."""
        return obj.users.count()


class RoleCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления роли.
    """
    class Meta:
        model = Role
        fields = (
            'id',
            'name',
            'description'
        )
        read_only_fields = ('id',)

    def validate_name(self, value):
        """Проверяет уникальность имени роли."""
        instance = self.instance
        if instance:
            # При обновлении исключаем текущий объект
            existing_role = Role.objects.filter(
                name=value
            ).exclude(pk=instance.pk).first()
        else:
            # При создании проверяем все роли
            existing_role = Role.objects.filter(name=value).first()

        if existing_role:
            raise serializers.ValidationError(
                'Роль с таким именем уже существует.'
            )

        return value


class BusinessElementSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения бизнес-элемента.
    """
    rules_count = serializers.SerializerMethodField()

    class Meta:
        model = BusinessElement
        fields = (
            'id',
            'name',
            'description',
            'rules_count',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'rules_count')

    def get_rules_count(self, obj):
        """Возвращает количество правил доступа для этого элемента."""
        return obj.access_rules.count()


class BusinessElementCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления бизнес-элемента.
    """
    class Meta:
        model = BusinessElement
        fields = (
            'id',
            'name',
            'description'
        )
        read_only_fields = ('id',)

    def validate_name(self, value):
        """Проверяет уникальность имени элемента."""
        instance = self.instance
        if instance:
            # При обновлении исключаем текущий объект
            existing_element = BusinessElement.objects.filter(
                name=value
            ).exclude(pk=instance.pk).first()
        else:
            # При создании проверяем все элементы
            existing_element = BusinessElement.objects.filter(name=value).first()

        if existing_element:
            raise serializers.ValidationError(
                'Бизнес-элемент с таким именем уже существует.'
            )

        return value