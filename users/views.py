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


class UserProfileView(APIView):
    """
    API endpoint для работы с профилем пользователя.

    GET /api/users/profile/ - получение профиля текущего пользователя
    PUT/PATCH /api/users/profile/ - обновление профиля
    DELETE /api/users/profile/ - мягкое удаление аккаунта
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Возвращает профиль текущего пользователя."""
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request):
        """Полное обновление профиля пользователя."""
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            # Возвращаем обновленные данные через UserProfileSerializer
            user_data = UserProfileSerializer(user).data
            return Response(
                {
                    'user': user_data,
                    'message': 'Профиль успешно обновлен'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request):
        """Частичное обновление профиля пользователя."""
        user = request.user
        serializer = UserProfileUpdateSerializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            # Возвращаем обновленные данные через UserProfileSerializer
            user_data = UserProfileSerializer(user).data
            return Response(
                {
                    'user': user_data,
                    'message': 'Профиль успешно обновлен'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):
        """Мягкое удаление аккаунта пользователя."""
        user = request.user

        # Мягкое удаление: устанавливаем is_active=False
        user.is_active = False
        user.save()

        return Response(
            {
                'message': 'Аккаунт успешно удален. Вы больше не можете войти в систему.'
            },
            status=status.HTTP_200_OK
        )


class UserLogoutView(APIView):
    """
    API endpoint для выхода из системы.

    POST /api/users/logout/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Выход из системы.

        В текущей реализации JWT токены stateless, поэтому просто
        возвращаем успешный ответ. Клиент должен удалить токен на своей стороне.
        В будущем можно добавить blacklist токенов.
        """
        return Response(
            {
                'message': 'Успешный выход из системы'
            },
            status=status.HTTP_200_OK
        )

