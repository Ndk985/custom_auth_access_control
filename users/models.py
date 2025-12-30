from django.db import models
from django.conf import settings
import bcrypt
import jwt
from datetime import datetime, timedelta


class User(models.Model):
    """
    Кастомная модель пользователя системы.
    
    Используется для аутентификации и авторизации.
    Email используется как username для входа в систему.
    """
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя',
        help_text='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия',
        help_text='Фамилия пользователя'
    )
    middle_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Отчество',
        help_text='Отчество пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        db_index=True,
        verbose_name='Email',
        help_text='Email адрес (используется для входа в систему)'
    )
    password_hash = models.CharField(
        max_length=128,
        verbose_name='Хеш пароля',
        help_text='Хеш пароля, созданный с помощью bcrypt'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Указывает, может ли пользователь войти в систему. '
                  'Используется для мягкого удаления.'
    )
    role = models.ForeignKey(
        'access.Role',
        on_delete=models.PROTECT,
        related_name='users',
        db_index=True,
        verbose_name='Роль',
        help_text='Роль пользователя в системе'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']
        db_table = 'users_user'

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        """
        Устанавливает пароль пользователя, хешируя его с помощью bcrypt.
        
        Args:
            raw_password: Пароль в открытом виде
        """
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(
            raw_password.encode('utf-8'),
            salt
        ).decode('utf-8')

    def check_password(self, raw_password):
        """
        Проверяет, соответствует ли переданный пароль хешу в БД.
        
        Args:
            raw_password: Пароль в открытом виде для проверки
            
        Returns:
            bool: True если пароль верный, False в противном случае
        """
        if not self.password_hash:
            return False
        try:
            return bcrypt.checkpw(
                raw_password.encode('utf-8'),
                self.password_hash.encode('utf-8')
            )
        except (ValueError, TypeError):
            return False

    def generate_jwt_token(self):
        """
        Генерирует JWT токен для пользователя.
        
        Returns:
            str: JWT токен в виде строки
        """
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow(),
        }
        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return token
