from django.urls import path
from django.views.generic import TemplateView

from ..views.servicces import listServices

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('services/list',listServices,name='list_services')
]
