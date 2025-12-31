"""
Middleware для установки request.user из JWT токена.
"""
from .utils import extract_token_from_header, get_user_from_token


class JWTAuthenticationMiddleware:
    """
    Middleware для автоматической установки request.user из JWT токена.

    Извлекает токен из заголовка Authorization: Bearer {token}
    и устанавливает request.user для всех запросов.

    Порядок в MIDDLEWARE должен быть после SessionMiddleware
    и перед обработкой views.
    """

    def __init__(self, get_response):
        """
        Инициализация middleware.

        Args:
            get_response: Callable для получения response от следующего middleware/view
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Обработка запроса.

        Args:
            request: HTTP запрос

        Returns:
            HTTP response
        """
        # Извлекаем токен из заголовка
        authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
        token = extract_token_from_header(authorization_header)

        # Если токен найден, пытаемся получить пользователя
        if token:
            user = get_user_from_token(token)
            if user:
                request.user = user
            else:
                # Если токен невалиден, устанавливаем AnonymousUser
                from django.contrib.auth.models import AnonymousUser
                request.user = AnonymousUser()
        else:
            # Если токена нет, оставляем request.user как есть
            # (может быть установлен другими middleware)
            pass

        response = self.get_response(request)
        return response
