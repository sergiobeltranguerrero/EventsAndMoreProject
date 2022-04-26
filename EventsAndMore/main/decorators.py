from django.shortcuts import render

from main.models import Cliente, Assignacion, Evento, Stand, Orden_Servicios


def cliente_only(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_cliente:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'error/error_generico.html', {'error': {
                'title': 'Sin permiso',
                'message': 'Acceso excusivo para el cliente'
            }})

    return wrap


def gestor_solicitudes_only(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_gestor_solicitudes:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'error/error_generico.html', {'error': {
                'title': 'Sin permiso',
                'message': 'Acceso excusivo para el gestor de solicitudes'
            }})

    return wrap


def servicios_adiciones_only(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_servicios_adiciones:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'error/error_generico.html', {'error': {
                'title': 'Sin permiso',
                'message': 'Acceso excusivo para el personal de servicios adicionales'
            }})

    return wrap


def organizador_eventos_only(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_organizador_eventos:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'error/error_generico.html', {'error': {
                'title': 'Sin permiso',
                'message': 'Acceso excusivo para el organizador de eventos'
            }})

    return wrap


def personal_direccion_only(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_personal_direccion:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'error/error_generico.html', {'error': {
                'title': 'Sin permiso',
                'message': 'Acceso excusivo para personal de dirección'
            }})

    return wrap


def event_is_validated(func):
    def wrap(request, *args, **kwargs):
        try:
            user = request.user
            client = Cliente.objects.get(user=user)
            if 'evento' in kwargs:
                id_evento = kwargs['evento']
            else:
                id_evento = request.POST['id_evento']

            if 'stand' in kwargs:
                id_stand = kwargs['stand']
            else:
                id_stand = request.POST['id_stand']

            if not Evento.objects.filter(id=id_evento).exists():
                return render(request, 'error/error_generico.html', {'error': {
                    'title': 'Evento no disponible',
                    'message': 'El evento no existe'
                }})

            if not Evento.objects.get(id=id_evento).activo:
                return render(request, 'error/error_generico.html', {'error': {
                    'title': 'Evento no disponible',
                    'message': 'El evento se encuentra desactivado o ha finalizado'
                }})

            if Assignacion.objects.filter(cliente=client, evento__id=id_evento, stand__id=id_stand).exists():
                asignacion = Assignacion.objects.get(cliente=client, evento__id=id_evento, stand__id=id_stand)
                if asignacion.es_valido_por_gestor and asignacion.es_valido_por_organizador_eventos:
                    return func(request, *args, **kwargs)

            return render(request, 'error/error_generico.html', {'error': {
                'title': 'Sin permiso',
                'message': 'No tienes permiso para acceder a este evento.',
            }})

        except KeyError:
            return render(request, 'error/error_generico.html', {'error': {
                'title': 'Algo a ido mal :(',
                'message': 'No tienes permiso para acceder a este evento.',
            }})

    return wrap


def reserva_realizada(func):
    def wrap(request, *args, **kwargs):
        try:
            if 'evento' in kwargs:
                id_evento = kwargs['evento']
            else:
                id_evento = request.POST['id_evento']
            if 'stand' in kwargs:
                id_stand = kwargs['stand']
            else:
                id_stand = request.POST['id_stand']

            evento = Evento.objects.get(pk=id_evento)
            stand = Stand.objects.get(pk=id_stand)
            cliente = Cliente.objects.get(user=request.user)

            if Orden_Servicios.objects.filter(cliente=cliente, evento=evento, stand=stand).exists():
                return render(request, 'error/error_generico.html', {'error': {
                    'title': 'Reserva ya realizada',
                    'message': 'Ya has realizado una reserva para este evento.',
                }})
            return func(request, *args, **kwargs)
        except KeyError:
            return render(request, 'error/error_generico.html', {'error': {
                'title': 'Algo a ido mal :(',
                'message': 'No tienes permiso para acceder a este evento.',
            }})
    return wrap
