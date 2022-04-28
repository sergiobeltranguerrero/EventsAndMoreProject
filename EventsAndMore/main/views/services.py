from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..models import Evento, Servicios_Especiales, Servicio, Cliente, Assignacion, Stand, Elementos_Carro
from main.cart import Cart

from main.decorators import cliente_only, event_is_validated, reserva_realizada


@cliente_only
@event_is_validated
@reserva_realizada
def services_view(request,**kwargs):
    id_evento = kwargs.get('evento')
    id_stand = kwargs.get('stand')
    user = request.user
    cliente = Cliente.objects.get(user=user)

    # Comprobamos que el stand está asignado al cliente y que el evento está activo
    if not Evento.objects.get(id=id_evento):
        return render(request, 'error/404.html')

    if not Assignacion.objects.filter(evento=id_evento, cliente=cliente, stand=id_stand).exists():
        return render(request, 'error/404.html')

    if not Assignacion.objects.get(evento=id_evento,    cliente=cliente, stand=id_stand).es_valido_por_gestor:
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
    for servicio in servicios_especiales:
        serv = servicio.servicio
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

def servicesAdd(request):
    if request.method == 'POST':
        name = request.POST['nombre']
        description = request.POST['descripcion']
        if request.POST['generic'] == "False":
            generic = False
        elif request.POST['generic'] == "True":
            generic = True
        else:
            return render(request,'services/add_service.html',{'succes':False})
        #imagen = "insertarFoto"
        price = int(request.POST['price'])
        aviable = True
        Servicio.objects.create(nombre=name,descripcion=description,precio=price,is_generic=generic,is_available=aviable)
        return HttpResponseRedirect(reverse('all_servicios'))
    else:
        return render(request,'services/add_service.html')

def services_set_aviable(request,**kwargs):
    id_service = kwargs.get('servicio')
    try:
        service = Servicio.objects.get(pk=id_service)
        service.is_available = True
        service.save()
        return HttpResponseRedirect(reverse('all_servicios'))
    except:
        return HttpResponseRedirect(reverse('all_servicios'))


def servicesDelete(request,**kwargs):
    id_service = kwargs.get('servicio')
    try:
        service = Servicio.objects.get(pk = id_service)
        service.is_available = False
        service.save()
        return HttpResponseRedirect(reverse('all_servicios'))
    except:
        return HttpResponseRedirect(reverse('all_servicios'))

def servicesListAll(request):
    if request.user.is_servicios_adicionales:
        servicios_genericos = Servicio.objects.filter(is_generic=True,is_available=True)
        servicios = Servicio.objects.filter(is_generic=False,is_available=True)
        servicios_no_aviable = Servicio.objects.filter(is_available=False)
        return render(request,'services/list_services.html',{'genericos':servicios_genericos, 'servicios': servicios,'not_aviable':servicios_no_aviable})
    else:
        return render(request,'error/error_generico.html')
