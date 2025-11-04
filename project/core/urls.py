from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("about/", TemplateView.as_view(template_name="core/about.html"), name="about"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(template_name="core/logout.html"), name="logout"),
    path("register/", register, name="register"),
    path('activar/<uidb64>/<token>/', activate, name="activate"),
]