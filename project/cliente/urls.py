from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cliente_list/", views.cliente_list, name="cliente_list"),
    path("cliente_create/", views.cliente_create, name="cliente_create"),
    # Aquí puedes agregar más rutas según sea necesario
]