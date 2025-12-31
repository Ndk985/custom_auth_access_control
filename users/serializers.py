"""
Сериализаторы для работы с пользователями.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=6,
        help_text='Пароль должен содержать минимум 6 символов'
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Повторите пароль'
    )

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'middle_name',
            'password', 'password_confirm', 'role'
        )
        extra_kwargs = {
            'email': {'required': True},
            'role': {'required': True},
        }

    def validate_email(self, value):
        """Проверяет уникальность email."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return value

    def validate(self, attrs):
        """Проверяет совпадение паролей."""
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({
                'password_confirm': 'Пароли не совпадают.'
            })

        return attrs

    def create(self, validated_data):
        """Создает нового пользователя."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для входа в систему."""
    email = serializers.EmailField(
        required=True,
        help_text='Email пользователя'
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Пароль пользователя'
    )

    def validate(self, attrs):
        """Проверяет email и пароль."""
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                'Email и пароль обязательны для заполнения.'
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Неверный email или пароль.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Аккаунт пользователя деактивирован.'
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                'Неверный email или пароль.'
            )

        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения профиля пользователя."""
    role_name = serializers.CharField(
        source='role.name',
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'middle_name',
            'is_active', 'role', 'role_name', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'email', 'is_active', 'created_at', 'updated_at'
        )


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления профиля пользователя."""

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'middle_name', 'role'
        )
        read_only_fields = ('id',)

    def validate_email(self, value):
        """Проверяет уникальность email (кроме текущего пользователя)."""
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return value
