"""
URL маршруты для приложения access.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccessRuleViewSet

app_name = 'access'

# Создаем router для ViewSet
router = DefaultRouter()
router.register(r'rules', AccessRuleViewSet, basename='accessrule')

urlpatterns = [
    path('', include(router.urls)),
]

