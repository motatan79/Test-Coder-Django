from django.db import models
from django.contrib.auth.models import User

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

class Equipo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipos_creados')

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    posicion1 = models.CharField(max_length=50)
    posicion2 = models.CharField(max_length=50)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre}" if self.apellido else self.nombre
    
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"