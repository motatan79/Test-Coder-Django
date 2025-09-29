from django.db import models

# Create your models here.

class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "país"
        verbose_name_plural = "países"
        ordering = ['nombre']

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    posicion1 = models.CharField(max_length=100, null=True, blank=True)
    posicion2 = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre}" if self.apellido else self.nombre