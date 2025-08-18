from django.urls import path
from .views import index

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    # Aquí puedes agregar más rutas según sea necesario
]