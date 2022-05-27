from django.db import models
from django.db.models import Model


class Encuesta(Model):
    nombre = models.CharField(max_length=50)
    evento = models.ForeignKey('Evento', on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    id_survey = models.CharField(max_length=50, unique=True, null=True, blank=True) # id de la encuesta en survey_monkey
    url_preview = models.URLField(null=True, blank=True)
    url_edit = models.URLField(null=True, blank=True)
    url_results = models.URLField(null=True, blank=True)
