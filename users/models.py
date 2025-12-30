from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
import bcrypt
import jwt
from datetime import datetime, timedelta


class UserManager(BaseUserManager):
    """Кастомный менеджер для модели User."""

    def create_user(self, email, password=None, **extra_fields):
        """Создает и возвращает обычного пользователя."""
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и возвращает суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        """Получает пользователя по email (username)."""
        return self.get(email=username)


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
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Персонал',
        help_text='Указывает, может ли пользователь войти в админ-панель Django.'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Суперпользователь',
        help_text='Указывает, что пользователь имеет все права без явного назначения.'
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

    # Обязательные атрибуты для кастомной модели пользователя Django
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Поля, требуемые при создании через createsuperuser

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']
        db_table = 'users_user'

    def __str__(self):
        return self.email

    @property
    def is_authenticated(self):
        """Всегда возвращает True для активных пользователей."""
        return self.is_active

    @property
    def is_anonymous(self):
        """Всегда возвращает False (не анонимный пользователь)."""
        return False

    @property
    def username(self):
        """Возвращает email как username для совместимости."""
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

    def has_perm(self, perm, obj=None):
        """
        Проверяет, имеет ли пользователь указанное разрешение.
        Для суперпользователя всегда возвращает True.
        """
        if self.is_active and self.is_superuser:
            return True
        return False

    def has_module_perms(self, app_label):
        """
        Проверяет, имеет ли пользователь разрешения для указанного приложения.
        Для суперпользователя всегда возвращает True.
        """
        if self.is_active and self.is_superuser:
            return True
        return False
