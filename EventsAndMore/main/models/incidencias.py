from django.db.models import Model
from django.db import models

from main.models.accounts import Cliente, Servicios_adicionales
from main.models.eventos import Evento


class Incidencia(Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    gestion = models.ForeignKey(Servicios_adicionales, on_delete=models.DO_NOTHING)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    ESTADO = [
        ('PD', 'Pendiente'),
        ('EP', 'En progreso'),
        ('SC', 'Solucionada'),
    ]
    estadoIn = models.CharField(max_length=2, choices=ESTADO, default=ESTADO[0][0])

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
