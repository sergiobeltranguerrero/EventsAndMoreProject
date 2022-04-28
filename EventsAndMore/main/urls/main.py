from django.urls import path
from django.views.generic import TemplateView

from EventsAndMore.settings import base as settings
from main.views import services_view
from main.views.accounts import RegisterClientView
from main.views.cart import remove_cart_element, show_cart_view, update_producto_view, reservation
from django.conf.urls.static import static
from main.views.cart import remove_cart_element, show_cart_view, update_producto_view
from main.views.incidences import NuevaIncidencia, Incidencias, detalles_incidencia, valorar_incidencia
from main.views.solicitudes import mostrar_assignaciones , detalles_assignacion
from main.views.client import show_info_client


urlpatterns_main = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register/client', RegisterClientView, name='register_client'),
    path('servicios/<int:evento>/<int:stand>', services_view, name='servicios'),
    path('client/info',show_info_client,name='info_client'),
    path('cart/<int:evento>/<int:stand>', show_cart_view, name='cart'),
    path('cart/delete/', remove_cart_element, name='remove_cart_element'),
    path('cart/update/', update_producto_view, name='update_product'),
    path('cart/reserve/', reservation, name='reserve'),
    path('incidencies/', Incidencias, name='incidencias'),
    path('incidencies/detalles/<int:id_incidencia>', detalles_incidencia,name='detalles_incidencia'),
    path('incidencies/valorar/<int:id_incidencia>', valorar_incidencia,name='valorar_incidencia'),
    path('incidencies/nueva/', NuevaIncidencia, name='nueva_incidencia'),
    path('assignaciones/', mostrar_assignaciones, name='mostrar_assignaciones'),
    path('assignaciones/detalles/<int:id_assignacion>', detalles_assignacion,name='detalles_assignacion'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
