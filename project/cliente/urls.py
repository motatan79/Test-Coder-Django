from django.urls import path
from . import views

app_name = "cliente"

urlpatterns = [
    path("", views.index, name="index"),
    path("cliente_list/", views.cliente_list, name="cliente_list"),
    path("alineacion_form/", views.alineacion_form, name="alineacion_form"),
    path("mi-equipo/", views.mi_equipo, name="mi_equipo"),
    path("crear-equipo/", views.crear_equipo, name="crear_equipo"),
]