from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер для модели пользователя."""

    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным именем пользователя.

        Параметры:
            username (str): Имя пользователя.
            password (str): Пароль пользователя (может быть None).
            extra_fields (dict): Дополнительные поля.
        """
        if not username:
            raise ValueError("Имя пользователя является обязательным")
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Создание и сохранение суперпользователя с указанным именем пользователя и паролем.

        Параметры:
        - username: Обязательное поле. Имя пользователя.
        - telegram_id: Обязательное поле. Уникальный идентификатор Telegram.
        - password: Пароль пользователя.
        - extra_fields: Дополнительные поля.
        """  # noqa: E501
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError(
                "Суперпользователь должен иметь is_superuser=True."
            )

        return self.create_user(
            username=username,
            password=password,
            **extra_fields,
        )

    def get_by_natural_key(self, username):
        """
        Получение пользователя по натуральному ключу (username).

        Параметры:
        - username: Имя пользователя.
        """
        return self.get(username=username)
