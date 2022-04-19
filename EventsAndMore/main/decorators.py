from django.shortcuts import render


def client_only(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_cliente:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'sin_permiso.html')

    return wrap


def gestor_solicitudes_only(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_gestor_solicitudes:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'sin_permiso.html')

    return wrap


def servicios_adiciones_only(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_servicios_adiciones:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'sin_permiso.html')

    return wrap


def organizador_eventos_only(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_organizador_eventos:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'sin_permiso.html')

    return wrap


def personal_direccion_only(func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_personal_direccion:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'sin_permiso.html')

    return wrap
