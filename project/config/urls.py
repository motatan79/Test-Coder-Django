
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("core.urls", "core"))),
    path("clientes/", include(("cliente.urls", "cliente"))),
    path("productos/", include(("producto.urls", "producto"))),
    path('', include('pwa.urls')),
    # Aquí puedes agregar más rutas según sea necesario
]
