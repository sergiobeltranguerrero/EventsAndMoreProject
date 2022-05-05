from django.urls import path
from django.views.generic import TemplateView

from EventsAndMore.settings import base as settings
from main.views import services_view
from main.views.accounts import RegisterClientView
from main.views.cart import remove_cart_element, show_cart_view, update_producto_view, reservation
from django.conf.urls.static import static
from main.views.cart import remove_cart_element, show_cart_view, update_producto_view
from main.views.incidences import NuevaIncidencia, Incidencias, detalles_incidencia
from main.views.solicitudes import mostrar_assignaciones , detalles_assignacion


urlpatterns_main = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register/client', RegisterClientView, name='register_client'),
    path('incidencies/', Incidencias, name='incidencias'),
    path('incidencies/detalles/<int:id_incidencia>', detalles_incidencia,name='detalles_incidencia'),
    path('incidencies/nueva/', NuevaIncidencia, name='nueva_incidencia'),
    path('assignaciones/', mostrar_assignaciones, name='mostrar_assignaciones'),
    path('assignaciones/detalles/<int:id_assignacion>', detalles_assignacion,name='detalles_assignacion'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
