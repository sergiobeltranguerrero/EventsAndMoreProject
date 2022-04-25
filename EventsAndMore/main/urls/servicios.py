from django.urls import path

from main.views import services_view, show_cart_view, remove_cart_element, update_producto_view, reservation

urlpatterns_servicios = [
    path('servicios/<int:evento>/<int:stand>', services_view, name='servicios'),
    path('cart/<int:evento>/<int:stand>', show_cart_view, name='cart'),
    path('cart/delete/', remove_cart_element, name='remove_cart_element'),
    path('cart/update/', update_producto_view, name='update_product'),
    path('cart/reservar/', reservation, name='reservar'),
]
