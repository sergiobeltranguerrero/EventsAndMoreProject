from django.db.models import Model
from django.db import models

# Create your models here.

class Servicios(Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)

class Sector(Model):
    nombre = models.CharField(max_length=50)

class Incidencia(Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    #usuario = models.ForeignKey(Usuario)

class Comentario(Model):
    incidencia = models.ForeignKey(Incidencia,on_delete=models.DO_NOTHING)
    asunto = models.CharField(max_length=100)
    cuerpo = models.CharField(max_length=500)
