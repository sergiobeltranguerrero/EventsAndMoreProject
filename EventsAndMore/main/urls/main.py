from django.urls import path
from django.views.generic import TemplateView

from ..views.accounts import RegisterClientView
from ..views.servicces import listServices
from ..views.accounts import RegisterClientView
from ..views.client import show_info_client
from ..views.cart import remove_cart_element, show_cart_view, update_producto_view


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register/client', RegisterClientView, name='register_client'),
    path('servicios/<int:evento>/<int:stand>', listServices, name='evento_servicios'),
    path('client/info',show_info_client,name='info_client'),
    path('cart/<int:evento>/<int:stand>', show_cart_view, name='cart'),
    path('cart/remove/<int:id_producto>', remove_cart_element, name='remove_cart_element'),
    path('cart/update/', update_producto_view, name='update_product'),
]
