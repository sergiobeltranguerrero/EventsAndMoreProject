from django.shortcuts import render

from main.models import Evento, Servicios_Especiales, Servicio
from carton.cart import Cart


def services_view(request, **kwargs):
    id_evento = kwargs.get('evento')

    # Buscaremos los servicios que tiene asignado el evento y el sector del cliente
    evento = Evento.objects.filter(id=id_evento)
    servicios_especiales = Servicios_Especiales.objects.filter(evento=evento[0])
    lista_servicios_especiales = [servicio.servicio for servicio in servicios_especiales]
    lista_servicios_genericos = list(Servicio.objects.filter(is_generic=True))
    lista_servicios = lista_servicios_genericos + lista_servicios_especiales

    if request.method == 'GET':
        return render(request, 'services/event_services.html', {'lista_servicios': lista_servicios})

    if request.method == 'POST':
        servicio = Servicio.objects.get(id=request.POST.get('id_servicio'))
        precio = servicio.precio

        cart = Cart(request.session)
        cart.add(servicio, price=precio)

        return render(request, 'services/event_services.html',
                      {'lista_servicios_especiales': lista_servicios_especiales, 'lista_servicios': lista_servicios})
