

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin_url = "/"  # Puedes cambiar esto para mayor seguridad

urlpatterns = [
    path("tla-ctrl-982x-panel/", admin.site.urls),
    path("", include(("core.urls", "core"))),
    path("clientes/", include(("cliente.urls", "cliente"))),
    path("productos/", include(("producto.urls", "producto"))),
    path('', include('pwa.urls')),
    # Aquí puedes agregar más rutas según sea necesario
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
