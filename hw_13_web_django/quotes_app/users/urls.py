from django.urls import path, include
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetCompleteView,
)
from .views import *


urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("reset-password/", ResetPasswordView.as_view(), name="password_reset"),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        ResetPasswordConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
