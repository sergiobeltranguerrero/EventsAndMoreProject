from django.db.models import Model
from django.db import models

from main.models.accounts import Cliente


class Incidencia(Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre + ' (' + str(self.id) + ')'


class Comentario(Model):
    incidencia = models.ForeignKey(Incidencia, on_delete=models.DO_NOTHING)
    asunto = models.CharField(max_length=100)
    cuerpo = models.CharField(max_length=500)

    def __str__(self):
        return self.asunto + ' (' + str(self.id) + ')'


class Estado_Incidencia(Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre + ' (' + str(self.id) + ')'


class Historial_Incidencias(Model):
    comentario = models.ForeignKey(Comentario, on_delete=models.DO_NOTHING)
    incidencia = models.ForeignKey(Incidencia, on_delete=models.DO_NOTHING)
    estado = models.ForeignKey(Estado_Incidencia, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    def __str__(self):
        return str(self.incidencia) + str(self.estado) + ' (' + str(self.id) + ')'
