from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cliente_list/", views.cliente_list, name="cliente_list"),
    # Aquí puedes agregar más rutas según sea necesario
]