from django.shortcuts import render

from main.models import Cliente, Assignacion, Evento, Stand, Orden_Servicios, User


def rols_required(*rols):
    """
    Decorador que verifica que el usuario tenga los roles requeridos. Para usarlo, se debe pasar una lista de roles
    como el siguiente ejemplo:
    @rols_required('servicios_adicionales', ['personal_direccion', 'cliente']) -> servicios_adicionales AND (personal_direccion OR cliente)
    @param rols: lista de roles requeridos ('visitante', 'cliente', 'gestor_solicitudes', 'servicios_adicionales', 'organizador_eventos', 'personal_direccion')
    """

    def decorator(func):
        def inner(request, *args, **kwargs):
            if request.user.is_authenticated:
                is_valid = True
                if len(rols) > 0:
                    for rol in rols:
                        if isinstance(rol, list):
                            temporal_valid = False
                            for r in rol:
                                if request.user.has_perm(r):
                                    temporal_valid = True
                                    break
                            is_valid = is_valid and temporal_valid
                        elif not request.user.has_perm(rol):
                            is_valid = False
                            break

                if is_valid:
                    return func(request, *args, **kwargs)
                else:
                    return render(request, 'error/error_generico.html', {'error': {
                        'title': 'Sin permisos',
                        'message': 'No tienes permiso para acceder.',
                    }})
            else:
                if any('visitante' in rol for rol in rols):
                    return func(request, *args, **kwargs)
                else:
                    return render(request, 'error/error_generico.html', {'error': {
                        'title': 'Sin permisos',
                        'message': 'No tienes permiso para acceder.',
                    }})

        return inner

    return decorator


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

def gestor_solicitudes_and_cliente(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_gestor_solicitudes or user.is_authenticated and user.is_cliente:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'error/error_generico.html', {'error': {
                'title': 'Esta pagina no existe',
                'message': 'O usted no tiene los permisos necesarios'
            }})

    return wrap

def servicios_adiciones_and_cliente(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_servicios_adicionales or user.is_authenticated and user.is_cliente:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'error/error_generico.html', {'error': {
                'title': 'Esta pagina no existe',
                'message': 'O usted no tiene los permisos necesarios'
            }})

    return wrap

def servicios_adicionales(func):
    def wrap(request, *args,**kwargs):
        user = request.user
        if user.is_authenticated and user.is_servicios_adicionales:
            return func(request,*args,**kwargs)
        else:
            return render(request,'error/error_generico.html', {'error': {
                'title' : 'Esta pagina no existe',
                'message': 'O usted no tiene los permisos necesarios'
            }})
    return wrap