from django.db import models
from django.utils import timezone

# Create your models here.

class ProductoCategoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True, verbose_name="descripcion", max_length=1000)   
    precio = models.FloatField()
    stock = models.IntegerField()

    def __str__(self) -> str:
        return self.nombre  
    
    class Meta:
        verbose_name = "ProductoCategoria"
        verbose_name_plural = "ProductoCategorias"
        ordering = ['id']
        
class Producto(models.Model):
    categoria_id = models.ForeignKey(ProductoCategoria, null= True, blank=True, on_delete=models.SET_NULL)
    nombre = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=50)
    stock = models.IntegerField()
    precio = models.FloatField()
    descripcion = models.TextField(null=True, blank=True, verbose_name="descripcion", max_length=1000)
    fecha_creacion = models.DateField(null=True, blank=True, default=timezone.now, editable=False, verbose_name="fecha de actualizacion")
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.unidad_medida}) ${self.precio:.2f}"
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['id']