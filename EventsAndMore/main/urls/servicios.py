from django.urls import path

from main.views import services_view, show_cart_view, remove_cart_element, update_producto_view, reservation, \
    request_new_services, solicitud_realizada, check_services, check_services_detail

urlpatterns_servicios = [
    path('servicios/<int:evento>/<int:stand>/', services_view, name='servicios'),
    path('cart/<int:evento>/<int:stand>/', show_cart_view, name='cart'),
    path('cart/delete/', remove_cart_element, name='remove_cart_element'),
    path('cart/update/', update_producto_view, name='update_product'),
    path('cart/reservar/', reservation, name='reservar'),
    path('solicitar/servicios/<int:evento>/', request_new_services, name='solicitar_servicios'),
    path('solicitar/servicios/<int:evento>/solicitado/', solicitud_realizada, name='solicitud_realizada'),
    path('check/servicios',check_services,name='check_services'),
    path('check/servicios/<int:solicitud>/detail',check_services_detail,name='check_services_detail')
]
