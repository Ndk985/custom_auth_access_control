"""
Кастомные authentication backends для работы с bcrypt паролями и JWT токенами.
"""
from django.contrib.auth.backends import BaseBackend
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .utils import extract_token_from_header, get_user_from_token


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


class JWTAuthentication(BaseAuthentication):
    """
    Authentication класс для Django REST Framework, использующий JWT токены.

    Извлекает токен из заголовка Authorization: Bearer {token}
    и устанавливает request.user для аутентифицированных пользователей.
    """

    def authenticate(self, request):
        """
        Аутентифицирует пользователя по JWT токену из заголовка.

        Args:
            request: HTTP запрос

        Returns:
            tuple: (user, token) если аутентификация успешна, None в противном случае

        Raises:
            AuthenticationFailed: Если токен невалиден или истек
        """
        authorization_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not authorization_header:
            return None

        token = extract_token_from_header(authorization_header)
        if not token:
            return None

        user = get_user_from_token(token)
        if not user:
            raise AuthenticationFailed('Невалидный или истекший токен')

        return (user, token)

    def authenticate_header(self, request):
        """
        Возвращает значение заголовка WWW-Authenticate для 401 ответа.

        Args:
            request: HTTP запрос

        Returns:
            str: Значение заголовка
        """
        return 'Bearer'

