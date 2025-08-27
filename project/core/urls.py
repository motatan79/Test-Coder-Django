from django.urls import path
from .views import index, about

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    # Aquí puedes agregar más rutas según sea necesario
]