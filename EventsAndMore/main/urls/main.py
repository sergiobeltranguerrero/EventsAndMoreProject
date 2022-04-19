from django.urls import path
from django.views.generic import TemplateView

from ..views.servicces import listServices
from ..views.client import show_info_client

urlpatterns = [
    path('', TemplateView.as_view(template_name='home_base.html'), name='home'),
    path('servicios/<int:evento>',listServices,name = 'service_to_client'),
    path('client/info',show_info_client,name = 'info_to_client')
]
