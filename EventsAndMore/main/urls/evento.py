from django.urls import path
from main.views import evento, solicitudes
from main.views.solicitudes import solicitudes_realizadas

urlpatterns_event = [
    path('evento/list_events', evento.list_events, name='list_events'),
    path('evento/detail_event/<int:id>', evento.detail_event, name='detail_event'),
    path('evento/my_events', evento.my_events, name='my_events'),
    path('evento/event_apply',solicitudes.solicitudes_eventos, name='solicitudes_eventos'),
    path('evento/new_event',evento.new_event,name='new_event'),
    path('solicitudes/organizador', solicitudes_realizadas, name='solicitudes_organizador')
    ]