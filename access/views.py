"""
API views для работы с правилами доступа.
"""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AccessRule
from .serializers import (
    AccessRuleSerializer,
    AccessRuleCreateUpdateSerializer
)
from .permissions import IsAdminRole


class AccessRuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления правилами доступа.

    Доступ разрешен только пользователям с ролью 'admin'.
    """
    queryset = AccessRule.objects.select_related('role', 'element').all()
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора в зависимости от действия.
        """
        if self.action in ('create', 'update', 'partial_update'):
            return AccessRuleCreateUpdateSerializer
        return AccessRuleSerializer

    def list(self, request):
        """
        GET /api/access/rules/
        Возвращает список всех правил доступа.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        GET /api/access/rules/{id}/
        Возвращает детали конкретного правила доступа.
        """
        try:
            access_rule = self.get_object()
            serializer = self.get_serializer(access_rule)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccessRule.DoesNotExist:
            return Response(
                {'detail': 'Правило доступа не найдено.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        """
        POST /api/access/rules/
        Создает новое правило доступа.
        """
        serializer = AccessRuleCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            access_rule = serializer.save()
            # Возвращаем созданное правило через AccessRuleSerializer
            response_serializer = AccessRuleSerializer(access_rule)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk=None):
        """
        PUT /api/access/rules/{id}/
        Полное обновление правила доступа.
        """
        try:
            access_rule = self.get_object()
            serializer = AccessRuleCreateUpdateSerializer(
                access_rule,
                data=request.data
            )

            if serializer.is_valid():
                serializer.save()
                # Возвращаем обновленное правило через AccessRuleSerializer
                response_serializer = AccessRuleSerializer(access_rule)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except AccessRule.DoesNotExist:
            return Response(
                {'detail': 'Правило доступа не найдено.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request, pk=None):
        """
        PATCH /api/access/rules/{id}/
        Частичное обновление правила доступа.
        """
        try:
            access_rule = self.get_object()
            serializer = AccessRuleCreateUpdateSerializer(
                access_rule,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()
                # Возвращаем обновленное правило через AccessRuleSerializer
                response_serializer = AccessRuleSerializer(access_rule)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except AccessRule.DoesNotExist:
            return Response(
                {'detail': 'Правило доступа не найдено.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        """
        DELETE /api/access/rules/{id}/
        Удаляет правило доступа.
        """
        try:
            access_rule = self.get_object()
            access_rule.delete()
            return Response(
                {'message': 'Правило доступа успешно удалено.'},
                status=status.HTTP_200_OK
            )
        except AccessRule.DoesNotExist:
            return Response(
                {'detail': 'Правило доступа не найдено.'},
                status=status.HTTP_404_NOT_FOUND
            )
