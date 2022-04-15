from carton.cart import Cart
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from main.models import Servicio


@login_required
def show_cart_view(request):
    cart = Cart(request.session)
    return render(request, 'services/cart.html', {'cart': cart})


@login_required
def remove_cart_element(request, id_producto):
    cart = Cart(request.session)
    service = Servicio.objects.get(id=id_producto)
    cart.remove(service)
    return render(request, 'services/cart.html', {'cart': cart})


@login_required
def update_producto_view(request):
    if request.POST:
        try:
            cart = Cart(request.session)
            id_product = request.POST['id_product']
            service = Servicio.objects.get(id=id_product)
            quantity = request.POST['quantity']
            cart.set_quantity(service, quantity)

            return JsonResponse({'status': 'ok',
                                 'total': cart.total,
                                 })

        except KeyError:
            return HttpResponseRedirect(reverse('cart'))

    return HttpResponseRedirect(reverse('cart'))
