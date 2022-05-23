from django.shortcuts import render

from main.models import Evento, Servicios_Especiales, Servicio, Cliente, Assignacion, Stand, \
    Organizador_Eventos, Servicio_Necesario, Solicitud_Servicios_Evento
from main.utils import Cart

from main.decorators import event_is_validated, reserva_realizada, rols_required


@event_is_validated
@reserva_realizada
def services_view(request, **kwargs):
    id_evento = kwargs.get('evento')
    id_stand = kwargs.get('stand')
    user = request.user
    cliente = Cliente.objects.get(user=user)

    # Comprobamos que el stand está asignado al cliente y que el evento está activo
    if not Evento.objects.get(id=id_evento):
        return render(request, 'error/404.html')

    if not Assignacion.objects.filter(evento=id_evento, cliente=cliente, stand=id_stand).exists():
        return render(request, 'error/404.html')

    if not Assignacion.objects.get(evento=id_evento, cliente=cliente, stand=id_stand).es_valido_por_gestor:
        return render(request, 'error/404.html')

    if not Assignacion.objects.get(evento=id_evento, cliente=cliente, stand=id_stand).es_valido_por_organizador_eventos:
        return render(request, 'error/404.html')

    # Comprobamos que el evento está activo
    evento = Evento.objects.get(id=id_evento)
    if not evento.activo:
        return render(request, 'error/404.html')

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

# Servicios que solicita el organizador de eventos para su evento.
@rols_required('organizador_eventos')
def request_new_services(request, **kwargs):
    id_evento = kwargs.get('evento')
    organizador = Organizador_Eventos.objects.get(user=request.user)
    solicitud = Solicitud_Servicios_Evento.objects.get_or_create(organizador=organizador, evento_id=id_evento)[0]
    servicios = list(Servicio.objects.filter(is_generic=True))
    servicios_selecionados = list(
        Servicio_Necesario.objects.filter(solicitud=solicitud, is_added=False).values_list('servicio', flat=True))
    servicios_necesarios = list(Servicio_Necesario.objects.filter(solicitud=solicitud, is_added=True))

    if request.method == 'GET':
        return render(request, 'services/request_new_services.html', {'servicios': servicios,
                                                                      'servicios_selecionados': servicios_selecionados,
                                                                      'servicios_necesarios': servicios_necesarios,
                                                                      'evento': Evento.objects.get(id=id_evento)})

    if request.method == 'POST':
        type = request.POST.get('type')
        servicio = Servicio.objects.filter(nombre=request.POST.get('servicio'))
        if type == 'Solicitar':
            Servicio_Necesario.objects.create(solicitud=solicitud, servicio=servicio[0])
            return JsonResponse({'status': 'ok'})
        elif type == 'Cancelar':
            Servicio_Necesario.objects.filter(solicitud=solicitud, servicio=servicio[0])[0].delete()
            return JsonResponse({'status': 'ok'})

        elif type == 'Nuevo_Servicio':
            service = request.POST.get('service_name')
            description = request.POST.get('service_description')
            if not service.strip():
                return JsonResponse({'status': 'error', 'message': 'El nombre del servicio no puede estar vacio'})

            if Servicio.objects.filter(nombre=service, is_generic=True).exists():
                return JsonResponse({'status': 'error', 'message': 'El servicio ya existe'})

            new_service = Servicio.objects.create(nombre=service, descripcion=description, is_generic=False,
                                                  is_new=True)
            Servicio_Necesario.objects.create(solicitud=solicitud, servicio=new_service, is_added=True)
            return JsonResponse(
                {'status': 'ok', 'service_name': new_service.nombre, 'service_description': new_service.descripcion})

        elif type == 'Eliminar_Nuevo_Servicio':
            servicio_necesario = \
                Servicio_Necesario.objects.filter(solicitud=solicitud,
                                                  servicio__nombre=request.POST.get('service_name'),
                                                  is_added=True)[0]
            servicio_necesario.delete()
            servicio_necesario.servicio.delete()

            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error'})


def solicitud_realizada(request, **kwargs):
    id_evento = kwargs.get('evento')
    organizador = Organizador_Eventos.objects.get(user=request.user)
    solicitud = Solicitud_Servicios_Evento.objects.filter(organizador=organizador, evento_id=id_evento)[0]
    servicios_necesarios = Servicio_Necesario.objects.filter(solicitud=solicitud)

    if solicitud.solicitado:
        return render(request, 'error/error_generico.html', {'error': {
            'title': 'Ya has realizado la solicitud',
            'message': 'Ponte en contacto con el personal de soporte para modificar tu solicitud.'
        }})

    if not solicitud:
        return render(request, 'error/error_generico.html', {'error': {
            'title': 'No existe ninguna solicitud',
            'message': 'Debes solicitar un evento para realizar una solicitud.'
        }})
    solicitud.solicitado = True
    solicitud.save()

    return render(request, 'services/success_reservation_new_services.html',
                  {'solicitud': solicitud, 'servicios_necesarios': servicios_necesarios})
