from django.urls import path
from main.views import stand

urlpatterns_stand = [
    path('evento/stand_planning/<int:id_event>', stand.stand_planning, name='stand_planning'),
    path('evento/stand_planning_edit/<int:id_event>', stand.stand_planning_edit, name='stand_planning_edit'),
    path('stand/get_stand/<int:id_event>', stand.get_stands_by_sector_event, name='get_stand'),
    path('stand/my_stand/<int:id_event>', stand.my_stand, name='my_stand'),
]