import datetime

from django.db.models import Model
from django.db import models

from main.models.accounts import Sector, Organizador_Eventos, Gestor_solicitudes


class Evento(Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=2000)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    capacidad = models.IntegerField()
    activo = models.BooleanField(default=True)
    organizador = models.ForeignKey(Organizador_Eventos, on_delete=models.DO_NOTHING)
    fecha_solicitud = models.DateTimeField(default=datetime.datetime.now())
    Validado_gestor = models.BooleanField(default=False)
    gestor_validador = models.ForeignKey(Gestor_solicitudes, on_delete=models.DO_NOTHING, null=True,
                                         blank=True)  # gestor que acepta la solicitud

    def __str__(self):
        return self.nombre


class Stand(Model):
    numero_stand = models.IntegerField()

    def __str__(self):
        return str(self.numero_stand) + ' (' + str(self.id) + ')'


class Evento_Stand_Sector(Model):
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    stand = models.ForeignKey(Stand, on_delete=models.DO_NOTHING)
    sector = models.ForeignKey(Sector, on_delete=models.DO_NOTHING)
    SIZE = [
        ('GR', 'Grande'),
        ('MD', 'Mediano'),
        ('PQ', 'Pequeño'),
    ]
    stand_size = models.CharField(max_length=2, choices=SIZE)

    def __str__(self):
        return str(self.evento) + str(self.stand) + str(self.sector) + ' (' + str(self.id) + ')'

    class Meta:
        unique_together = (("evento", "stand", 'sector'),)
