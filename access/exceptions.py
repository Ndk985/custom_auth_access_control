"""
Кастомные исключения для системы доступа.
"""
from rest_framework import status
from rest_framework.exceptions import APIException


class UnauthorizedError(APIException):
    """
    Исключение для случая, когда пользователь не аутентифицирован.
    
    Возвращает HTTP 401 Unauthorized.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Требуется аутентификация.'
    default_code = 'authentication_required'


class ForbiddenError(APIException):
    """
    Исключение для случая, когда пользователь аутентифицирован,
    но не имеет доступа к запрашиваемому ресурсу.
    
    Возвращает HTTP 403 Forbidden.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Доступ запрещен.'
    default_code = 'permission_denied'

