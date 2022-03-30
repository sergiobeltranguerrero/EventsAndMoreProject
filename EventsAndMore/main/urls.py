from django.urls import path
from django.views.generic import TemplateView

from main.views import RegisterClientView, AdminView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
