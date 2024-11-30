from django.urls import path

from users.views import (
    LinkTelegramView,
    check_auth,
    home,
    login_view,
    logout_view,
)

urlpatterns = [
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("check-auth/", check_auth, name="check_auth"),
    path("link-telegram/", LinkTelegramView.as_view(), name="link_telegram"),
]
