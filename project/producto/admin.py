from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_title = "Productos"

class ProductoCategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
   
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("categoria_id", "nombre", "unidad_medida", "precio", "stock", "fecha_creacion", )   
    list_display_links = ("nombre",)
    search_fields = ("nombre",)
    list_filter = ("categoria_id", )
    ordering = ("categoria_id", "nombre")
    date_hierarchy = "fecha_creacion"

admin.site.register(ProductoCategoria, ProductoCategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)