from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from main.cart import Cart
from main.decorators import event_is_validated, cliente_only, reserva_realizada
from main.models import Cliente, Orden_Servicios, Elementos_Carro, Servicios_Orden, Evento, Stand


@cliente_only
@event_is_validated
@reserva_realizada
def show_cart_view(request, **kwargs):
    try:
        id_evento = kwargs.get('evento')
        id_stand = kwargs.get('stand')
        cliente = Cliente.objects.get(user=request.user)

        if request.method == 'GET':
            cart = Cart(evento=id_evento, stand=id_stand, cliente=cliente)
            return render(request, 'services/cart.html', {'cart': cart})

        return render(request, 'error/error_generico.html', {'error': {
            'title': 'Algo ha ido mal...',
            'message': 'No se ha podido mostrar el carrito.'
        }})
    except KeyError:
        return render(request, 'error/error_generico.html', {'error': {
            'title': 'ALgo ha ido mal :(',
            'message': 'No se ha podido mostrar el carrito'
        }})


@cliente_only
@event_is_validated
@reserva_realizada
def remove_cart_element(request):
    if request.POST:
        try:
            id_evento = request.POST.get('id_evento')
            id_stand = request.POST.get('id_stand')
            id_servicio = request.POST.get('id_servicio')
            cliente = Cliente.objects.get(user=request.user)
            cart = Cart(cliente=cliente, evento=id_evento, stand=id_stand)
            cart.remove(id_servicio)

            return HttpResponseRedirect(reverse('cart', kwargs={'evento': id_evento, 'stand': id_stand}))
        except KeyError:
            return HttpResponseRedirect(reverse('cart'))

    return HttpResponseRedirect(reverse('cart'))


@cliente_only
@event_is_validated
@reserva_realizada
def update_producto_view(request):
    if request.POST:
        try:
            id_evento = request.POST.get('id_evento')
            id_stand = request.POST.get('id_stand')
            id_servicio = request.POST.get('id_servicio')
            quantity = int(request.POST['quantity'])

            cliente = Cliente.objects.get(user=request.user)

            cart = Cart(cliente=cliente, evento=id_evento, stand=id_stand)
            cart.set_quantity(id_servicio, quantity)

            return JsonResponse({'status': 'ok', 'total': cart.total})
        except KeyError:
            return HttpResponseRedirect(reverse('cart'))

    return HttpResponseRedirect(reverse('cart'))


@cliente_only
@event_is_validated
@reserva_realizada
def reservation(request):
    try:
        if request.method == 'POST':
            id_evento = request.POST.get('id_evento')
            id_stand = request.POST.get('id_stand')
            evento = Evento.objects.get(pk=id_evento)
            stand = Stand.objects.get(pk=id_stand)
            cliente = Cliente.objects.get(user=request.user)

            cart = Cart(evento=evento, stand=stand, cliente=cliente)
            if cart.is_empty():
                return render(request, 'error/error_generico.html', {'error': {
                    'title': 'No hay productos en el carrito',
                    'message': 'No se puede realizar la reserva sin productos en el carrito.'
                }})

            orden = Orden_Servicios.objects.create(cliente=cliente, evento=evento, stand=stand)
            total = cart.total
            for element in cart.items:
                Servicios_Orden(orden=orden, servicio=element.servicio, cantidad=element.cantidad).save()

            cart.clear()
            servicios_orden = Servicios_Orden.objects.filter(orden=orden)

            return render(request, 'services/success_reservation.html',
                          {'servicios_orden': servicios_orden, 'total': total})

        return render(request, 'error/error_generico.html', {'error': {
            'title': 'Algo ha ido mal...',
            'message': 'No se ha podido realizar la reserva.'
        }})

    except KeyError:
        return render(request, 'error/error_generico.html', {'error': {
            'title': 'Algo ha ido mal :(',
            'message': 'No se ha podido realizar la reserva.'
        }})
