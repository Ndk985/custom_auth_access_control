"""
API views для работы с пользователями.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer
)
from .utils import generate_jwt_token

User = get_user_model()


class UserRegistrationView(APIView):
    """
    API endpoint для регистрации нового пользователя.

    POST /api/users/register/
    Body: {
        "email": "user@example.com",
        "password": "password123",
        "password_confirm": "password123",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "middle_name": "Отчество",
        "role": 1
    }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Регистрирует нового пользователя."""
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Генерируем JWT токен
            token = generate_jwt_token(user.id, user.email)

            # Возвращаем данные пользователя и токен
            user_data = UserProfileSerializer(user).data
            return Response(
                {
                    'user': user_data,
                    'token': token,
                    'message': 'Пользователь успешно зарегистрирован'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLoginView(APIView):
    """
    API endpoint для входа в систему.

    POST /api/users/login/
    Body: {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Аутентифицирует пользователя и возвращает JWT токен."""
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Генерируем JWT токен
            token = generate_jwt_token(user.id, user.email)

            # Возвращаем данные пользователя и токен
            user_data = UserProfileSerializer(user).data
            return Response(
                {
                    'user': user_data,
                    'token': token,
                    'message': 'Успешный вход в систему'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

