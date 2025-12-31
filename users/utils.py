"""
Утилиты для работы с JWT токенами.
"""
from django.conf import settings
from django.contrib.auth import get_user_model
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict

User = get_user_model()


def generate_jwt_token(user_id: int, email: str, expiration_hours: int = 24) -> str:
    """
    Генерирует JWT токен для пользователя.

    Args:
        user_id: ID пользователя
        email: Email пользователя
        expiration_hours: Время жизни токена в часах (по умолчанию 24)

    Returns:
        str: JWT токен в виде строки
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=expiration_hours),
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm='HS256'
    )
    # PyJWT 2.x возвращает строку, но для совместимости проверяем
    if isinstance(token, bytes):
        return token.decode('utf-8')
    return token


def decode_jwt_token(token: str) -> Optional[Dict]:
    """
    Декодирует и валидирует JWT токен.

    Args:
        token: JWT токен в виде строки

    Returns:
        dict: Payload токена если валиден, None в противном случае
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        # Токен истек
        return None
    except jwt.InvalidTokenError:
        # Невалидный токен
        return None


def get_user_from_token(token: str) -> Optional[User]:
    """
    Получает пользователя из JWT токена.

    Args:
        token: JWT токен в виде строки

    Returns:
        User: Объект пользователя если токен валиден, None в противном случае
    """
    payload = decode_jwt_token(token)
    if not payload:
        return None

    user_id = payload.get('user_id')
    if not user_id:
        return None

    try:
        user = User.objects.get(pk=user_id, is_active=True)
        return user
    except User.DoesNotExist:
        return None


def extract_token_from_header(authorization_header: str) -> Optional[str]:
    """
    Извлекает JWT токен из заголовка Authorization.

    Args:
        authorization_header: Значение заголовка Authorization
                             (формат: "Bearer {token}")

    Returns:
        str: Токен если найден, None в противном случае
    """
    if not authorization_header:
        return None

    parts = authorization_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None

    return parts[1]
