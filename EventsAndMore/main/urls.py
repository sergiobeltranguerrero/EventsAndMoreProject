from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register/client', views.RegisterClientView, name='register_client'),
    path('panel/admin', views.AdminView.as_view(), name='admin_panel'),
    path('evento/stand_planning/<int:id_event>', views.stand_planning, name='stand_planning'),
    path('stand/get_stand/<int:id_event>', views.get_stand, name='get_stand')
]
