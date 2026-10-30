
from django.db import models


class Pokemon(models.Model):
    nombre = models.CharField(max_length=100)
    peso = models.FloatField(default=0)
    imagen = models.URLField(blank=True, null=True)
    habilidades = models.TextField(default='')
    naturaleza = models.CharField(max_length=100, default='Desconocida')
    elemento = models.CharField(max_length=50, default='Desconocido')
    descripcion = models.TextField(default='')

    def __str__(self):
        return self.nombre


class Gimnasio(models.Model):
    lider_del_gym = models.CharField(max_length=100)
    naturaleza = models.CharField(max_length=100, default='Desconocida')
    elemento = models.CharField(max_length=50, default='Desconocido')
    medallas = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.lider_del_gym


class Entrenador(models.Model):
    id_documento = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    pokemones = models.ManyToManyField(
        'Pokemon',
        blank=True,
        related_name='entrenadores'
    )

    gimnasios = models.ManyToManyField(
        Gimnasio,
        blank=True,
        related_name='entrenadores',
        verbose_name='Gym'
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"