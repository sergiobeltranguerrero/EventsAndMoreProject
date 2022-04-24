from django.shortcuts import render

from main.models import Evento, Servicios_Especiales, Servicio, Cliente, Assignacion, Stand, Elementos_Carro
from main.cart import Cart


@cliente_only
@event_is_validated
@reserva_realizada
def listServices(request,**kwargs):
    id_evento = kwargs.get('evento')
    id_stand = kwargs.get('stand')
    user = request.user
    cliente = Cliente.objects.get(user=user)

    # Comprobamos que el stand está asignado al cliente y que el evento está activo
    if not Evento.objects.get(id=id_evento):
        return render(request, '404.html')

    if not Assignacion.objects.filter(evento=id_evento, cliente=cliente, stand=id_stand).exists():
        return render(request, '404.html')

    if not Assignacion.objects.get(evento=id_evento, cliente=cliente, stand=id_stand).es_valido_por_gestor:
        return render(request, '404.html')

    if not Assignacion.objects.get(evento=id_evento, cliente=cliente, stand=id_stand).es_valido_por_organizador_eventos:
        return render(request, '404.html')

    # Comprobamos que el evento está activo
    evento = Evento.objects.get(id=id_evento)
    if not evento.activo:
        return render(request, '404.html')

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

        servicios_carro = Cart(cliente=cliente, evento=evento, stand=stand)
        servicios_carro.add(servicio)

        return render(request, 'services/event_services.html', {'lista_servicios': lista_servicios,
                                                                'evento': evento,
                                                                'stand': stand})

    return render(request, 'services/event_services.html', {'lista_servicios': lista_servicios,
                                                            'evento': evento,
                                                            'stand': stand})

# TODO: Añadir la cantidad maxima que se puede adquirir de un servicio
