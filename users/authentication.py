"""
Кастомный authentication backend для работы с bcrypt паролями.
"""
from django.contrib.auth.backends import BaseBackend
from .models import User


class BcryptAuthenticationBackend(BaseBackend):
    """
    Authentication backend для кастомной модели User с bcrypt паролями.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Аутентифицирует пользователя по email и паролю.

        Args:
            request: HTTP запрос
            username: Email пользователя
            password: Пароль в открытом виде

        Returns:
            User объект если аутентификация успешна, None в противном случае
        """
        if username is None:
            username = kwargs.get('email')
        if username is None or password is None:
            return None

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if not user.is_active:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        """
        Получает пользователя по ID.

        Args:
            user_id: ID пользователя

        Returns:
            User объект или None
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

