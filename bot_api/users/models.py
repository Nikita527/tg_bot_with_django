import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.constants import MAX_NAME_LENGTH
from users.managers import CustomUserManager


def get_token_expiration():
    """Возвращает время истечения токена."""
    return timezone.now() + timedelta(minutes=15)


class AuthToken(models.Model):
    """Модель токена авторизации."""

    user = models.ForeignKey(
        to="users.User",
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
    )
    token = models.UUIDField(
        verbose_name=_("Токен"),
        default=uuid.uuid4,
        unique=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("Дата создания"),
        auto_now_add=True,
    )
    is_used = models.BooleanField(
        verbose_name=_("Использован"),
        default=False,
    )
    expires_at = models.DateTimeField(
        verbose_name=_("Срок действия"),
        default=get_token_expiration,
    )

    class Meta:
        verbose_name = "Токен авторизации"
        verbose_name_plural = "Токены авторизации"

    def __str__(self) -> str:
        """Возвращает username и Telegram ID пользователя."""
        return f"AuthToken for {self.user.username} - {self.token}"


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя."""

    first_name = models.CharField(
        verbose_name=_("Имя"),
        max_length=MAX_NAME_LENGTH,
    )
    last_name = models.CharField(
        verbose_name=_("Фамилия"),
        max_length=MAX_NAME_LENGTH,
    )
    telegram_id = models.BigIntegerField(
        verbose_name=_("ID в Telegram"),
        unique=True,
        blank=True,
        null=True,
    )
    username = models.CharField(
        verbose_name=_("Имя пользователя"),
        max_length=MAX_NAME_LENGTH,
        unique=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_("Статус персонала"),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_("Активный"),
        default=True,
    )
    is_superuser = models.BooleanField(
        verbose_name=_("Статус суперпользователя"),
        default=False,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self) -> str:
        """Возвращает username и Telegram ID пользователя."""
        return f"{self.username}"
