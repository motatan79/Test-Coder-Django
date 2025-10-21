from django.contrib import admin

# Register your models here.
from .models import Cliente, Pais, Equipo, Perfil

admin.site.register(Pais)
admin.site.register(Cliente)
admin.site.register(Equipo)
admin.site.register(Perfil)
