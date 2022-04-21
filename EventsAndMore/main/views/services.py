from django.shortcuts import render

from main.decorators import cliente_only, event_is_validated, reserva_realizada
from main.models import Evento, Servicios_Especiales, Servicio, Cliente, Assignacion, Stand, Elementos_Carro
from main.cart import Cart


@cliente_only
@event_is_validated
@reserva_realizada
def services_view(request, **kwargs):
    id_evento = kwargs.get('evento')
    id_stand = kwargs.get('stand')
    user = request.user
    cliente = Cliente.objects.get(user=user)

    stand = Stand.objects.get(id=id_stand)
    evento = Evento.objects.get(id=id_evento)

    servicios_especiales = Servicios_Especiales.objects.filter(evento=evento)
    lista_servicios_especiales = [servicio.servicio for servicio in servicios_especiales]
    lista_servicios_genericos = list(Servicio.objects.filter(is_generic=True))
    lista_servicios = lista_servicios_genericos + lista_servicios_especiales

    servicios_carro = Cart(cliente=cliente, evento=evento, stand=stand)

    if request.method == 'GET':
        return render(request, 'services/event_services.html', {'lista_servicios': lista_servicios,
                                                                'evento': evento,
                                                                'stand': stand})

    if request.method == 'POST':
        servicio = Servicio.objects.get(id=request.POST.get('id_servicio'))

        servicios_carro.add(servicio)

        return render(request, 'services/event_services.html', {'lista_servicios': lista_servicios,
                                                                'evento': evento,
                                                                'stand': stand})

    return render(request, 'services/event_services.html', {'lista_servicios': lista_servicios,
                                                            'evento': evento,
                                                            'stand': stand})

# TODO: Añadir la cantidad maxima que se puede adquirir de un servicio
