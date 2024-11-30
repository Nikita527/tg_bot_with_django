import os
import uuid

from rest_framework import generics, status
from rest_framework.response import Response

from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from users.models import AuthToken, User
from users.serializers import LinkTelegramSerializer


class LinkTelegramView(generics.CreateAPIView):
    """Представление для связывания Telegram-аккаунта с пользователем."""

    serializer_class = LinkTelegramSerializer

    def post(self, request, *args, **kwargs):
        """Связывание Telegram-аккаунта с пользователем."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data.get("token")
            telegram_id = serializer.validated_data.get("telegram_id")
            first_name = serializer.validated_data.get("first_name", "")
            last_name = serializer.validated_data.get("last_name", "")
            username = serializer.validated_data.get("username", "")

            try:
                auth_token = AuthToken.objects.select_related("user").get(
                    token=token, is_used=False
                )
                if auth_token.expires_at < timezone.now():
                    return Response(
                        {"message": "Срок действия токена истек."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user = auth_token.user
                user.telegram_id = telegram_id
                user.first_name = first_name
                user.last_name = last_name
                if username:
                    if (
                        User.objects.filter(username=username)
                        .exclude(id=user.id)
                        .exists()
                    ):
                        username = f"{username}_{telegram_id}"
                    user.username = username
                user.is_active = True
                user.save()
                auth_token.is_used = True
                auth_token.save()
                return Response(
                    {"message": "Telegram-аккаунт успешно связан."},
                    status=status.HTTP_200_OK,
                )
            except AuthToken.DoesNotExist:
                return Response(
                    {"message": "Неверный или использованный токен."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login_view(request):
    """Вход в систему."""
    if request.method == "GET":
        # Генерируем уникальный токен
        token = uuid.uuid4()
        if request.user.is_authenticated:
            user = request.user
        else:
            user = User.objects.create(
                username=str(token),
                is_active=False,
            )
        auth_token = AuthToken.objects.create(user=user, token=token)
        request.session["auth_token"] = str(auth_token.token)
        bot_username = os.environ.get("TELEGRAM_BOT_USERNAME")
        telegram_link = f"https://t.me/{bot_username}?start={token}"
        return render(request, "login.html", {"telegram_link": telegram_link})


def check_auth(request):
    """Проверка авторизации."""
    if request.user.is_authenticated:
        return JsonResponse({"is_authenticated": True})

    auth_token_value = request.session.get("auth_token")
    if auth_token_value:
        try:
            auth_token = AuthToken.objects.select_related("user").get(
                token=auth_token_value, is_used=True
            )
            user = auth_token.user
            login(request, user)
            request.session.pop("auth_token", None)
            return JsonResponse({"is_authenticated": True})
        except AuthToken.DoesNotExist:
            pass
    return JsonResponse({"is_authenticated": False})


def home(request):
    """Главная страница."""
    if request.user.is_authenticated:
        username = request.user.username or "Пользователь"
    else:
        username = "Гость"
    return render(request, "home.html", {"username": username})


def logout_view(request):
    logout(request)
    return redirect("home")
