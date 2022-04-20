from django.shortcuts import render

from main.models import Cliente, Assignacion, Evento


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
        user = request.user
        client = Cliente.objects.get(user=user)
        if not Evento.objects.filter(id=kwargs['evento']).exists():
            return render(request, 'error/error_generico.html', {'error': {
                'title': 'Evento no disponible',
                'message': 'El evento no existe'
            }})

        if not Evento.objects.get(id=kwargs['evento']).activo:
            return render(request, 'error/error_generico.html', {'error': {
                'title': 'Evento no disponible',
                'message': 'El evento se encuentra desactivado o ha finalizado'
            }})

        if Assignacion.objects.filter(cliente=client, evento__id=kwargs['evento'], stand__id=kwargs['stand']).exists():
            asignacion = Assignacion.objects.get(cliente=client, evento__id=kwargs['evento'], stand__id=kwargs['stand'])
            if asignacion.es_valido_por_gestor and asignacion.es_valido_por_organizador_eventos:
                return func(request, *args, **kwargs)

        return render(request, 'error/error_generico.html', {'error': {
            'title': 'Sin permiso',
            'message': 'No tienes permiso para acceder a este evento.',
        }})

    return wrap
