from django.urls import path
from main.views import evento

urlpatterns_event = [
    path('evento/list_events', evento.list_events, name='list_events'),
    path('evento/detail_event/<int:id>', evento.detail_event, name='detail_event'),
    ]