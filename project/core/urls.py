from django.urls import path
from .views import index

urlpatterns = [
    path("", index, name="index"),
    # Aquí puedes agregar más rutas según sea necesario
]