from django.urls import path

from main.views.encuestas import encuestas_creadas, encuestas_creadas_historial

urlpatterns_encuestas = [
    path('encuestas/creadas/', encuestas_creadas, name='encuestas_creadas'),
    path('encuestas/creadas/historial/', encuestas_creadas_historial, name='encuestas_creadas_historial')
]