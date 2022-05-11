from django.urls import path
from main.views import evento, solicitudes

urlpatterns_event = [
    path('evento/list_events', evento.list_events, name='list_events'),
    path('evento/detail_event/<int:id>', evento.detail_event, name='detail_event'),
    path('evento/my_events', evento.my_events, name='my_events'),
    path('evento',solicitudes.solicitudes_eventos, name='solicitudes_eventos')
    ]