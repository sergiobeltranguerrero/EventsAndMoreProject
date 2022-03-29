from django.urls import path
from django.views.generic import TemplateView

from main.views import RegisterClientView, AdminView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register/client', RegisterClientView, name='register_client'),
    path('panel/admin', AdminView.as_view(), name='admin_panel'),
]
