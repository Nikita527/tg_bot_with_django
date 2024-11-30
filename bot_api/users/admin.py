from django.contrib import admin

from users.models import AuthToken, User


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    """Модель токена авторизации."""

    list_display = ("user", "token", "created_at", "is_used")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    list_filter = ("is_used",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Кастомная модель администратора."""

    list_display = (
        "telegram_id",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    search_fields = ("username", "first_name", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active")
