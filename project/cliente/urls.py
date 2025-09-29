from django.urls import path
from . import views

app_name = "cliente"

urlpatterns = [
    path("", views.index, name="index"),
    path("cliente_list/", views.cliente_list, name="cliente_list"),
    path("cliente_create/", views.cliente_create, name="cliente_create"),
    
]