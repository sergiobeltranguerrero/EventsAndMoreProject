from django.urls import path

from main.views import informe_mensual_eventos

urlpatterns_informes = [
    path('informes/mensual/eventos/', informe_mensual_eventos, name='informe_mensual_eventos'),
]