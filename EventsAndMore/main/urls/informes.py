from django.urls import path

from main.views import informe_mensual_eventos, informe_mensual_beneficios

urlpatterns_informes = [
    path('informes/mensual/eventos/', informe_mensual_eventos, name='informe_mensual_eventos'),
    path('informes/mensual/beneficios/', informe_mensual_beneficios, name='informe_mensual_beneficios'),
]
