# en core/admin_security.py
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.urls import path

def staff_only(user):
    return user.is_active and user.is_staff

admin_view = user_passes_test(staff_only)(admin.site.login)

urlpatterns = [
    path("tla-ctrl-982x-panel/", admin_view),
]
admin.site.login = admin_view