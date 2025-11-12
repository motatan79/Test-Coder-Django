from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from .views import *
from django.urls import path, reverse_lazy

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    path("about/", TemplateView.as_view(template_name="core/about.html"), name="about"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(template_name="core/logout.html"), name="logout"),
    path("register/", register, name="register"),
    path('activar/<uidb64>/<token>/', activate, name="activate"),
    # 🔹 Recuperación de contraseña personalizada
    path(
        "password_reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        PasswordResetDoneView.as_view(template_name="core/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="core/password_reset_confirm.html",
            success_url=reverse_lazy("core:password_reset_complete"),
    ),
    name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(template_name="core/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]