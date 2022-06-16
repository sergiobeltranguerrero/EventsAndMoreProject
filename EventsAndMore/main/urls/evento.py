from django.urls import path
from main.views import evento, solicitudes,client
from main.views.solicitudes import solicitudes_realizadas

urlpatterns_event = [
    path('evento/list_events', evento.list_events, name='list_events'),
    path('evento/facturation_clients/<int:id>', client.client_facturation, name='facturation_event'),
    path('evento/detail_event/<int:id>', evento.detail_event, name='detail_event'),
    path('evento/my_events', evento.my_events, name='my_events'),
    path('evento/event_apply',solicitudes.solicitudes_eventos, name='solicitudes_eventos'),
    path('evento/new_event',evento.new_event,name='new_event'),
    path('solicitudes/organizador', solicitudes_realizadas, name='solicitudes_organizador'),
    path('evento/facturacion_eventos', evento.facturacion_eventos, name='facturacion_eventos'),
    path('evento/facturacion_evento/<int:id>', evento.facturacion_evento_detalle, name='facturacion_evento'),
    path('evento/show_event_facturation/<int:id>', evento.show_event_facturation, name='show_event_facturation'),
    path('evento/show_events_facturation/<int:id>', evento.show_events_facturation, name='show_events_facturation')
    ]