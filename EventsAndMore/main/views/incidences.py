# this lets the user create an incidence
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Incidencia, Cliente, Evento, Assignacion
from .evento import State
from main.decorators import servicios_adiciones_only, servicios_adiciones_and_cliente, cliente_only
from django.urls import reverse


@servicios_adiciones_and_cliente
def Incidencias(request):
    states = []
    for estado in Incidencia.ESTADO:
        states.append(State(estado[0], estado[1]))
    if request.method == 'POST':
        if not request.POST['state']== '%':
            cliente = Cliente.objects.get(user=request.user)
            incidencia = Incidencia.objects.filter(estadoIn = request.POST['state'], cliente_id=cliente.id)
        else:
            cliente = Cliente.objects.get(user=request.user)
            incidencia = Incidencia.objects.filter(cliente_id=cliente.id)
        return render(request, "incidencia/incidencia.html", {"incidencia": incidencia, 'states': states})

    if request.method == 'GET':
        cliente = Cliente.objects.get(user=request.user)
        incidencia = Incidencia.objects.filter(cliente_id=cliente.id)
        return render(request, "incidencia/incidencia.html", {"incidencia": incidencia, 'states': states})



@login_required()
def detalles_incidencia(request,id_incidencia):
    states = []
    for estado in Incidencia.ESTADO:
        states.append(State(estado[0], estado[1]))

        cliente = Cliente.objects.get(user=request.user)
        incidencia = Incidencia.objects.filter(id = id_incidencia)
        try:
            incidencia2 = Incidencia.objects.get(id = id_incidencia)
        except:
            return render(request, "error/error_generico.html", {'error': {
                'title': 'Esta pagina no existe',
                'message': 'O usted no tiene los permisos necesarios'
            }})
        if request.user.id == incidencia2.cliente.user.id:
            if not incidencia2.estadoIn == 'SC':
                return render(request,"incidencia/detalles_incidencia.html",{"indicencia" : incidencia, 'id' : incidencia[0].id, "cliente" : cliente, 'states': states, "descripcion" : incidencia[0].descripcion})
            else:
                return render(request, "error/error_generico.html",{'error':{
                    'title': 'Esta pagina no existe',
                    'message': 'O usted no tiene los permisos necesarios'
                }})
        else:
            return render(request, "error/error_generico.html", {'error': {
                'title': 'Esta pagina no existe',
                'message': 'O usted no tiene los permisos necesarios'
            }})



@cliente_only
def NuevaIncidencia(request):
    eventos_list = list()
    for assignaciones in Assignacion.objects.filter(cliente_id=request.user.id):
        eventos_list.append(assignaciones.evento)

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        if str.isdigit(request.POST['Evento']):
            event = Evento.objects.get(pk=request.POST['Evento'])
        else:
            return render(request, 'incidencia/nueva_incidencia.html', {'success': False, 'eventos': eventos_list})
        cliente = Cliente.objects.get(user=request.user)
        Incidencia.objects.create(nombre=nombre, descripcion=descripcion,estadoIn='PD', cliente=cliente, gestion_id=1,evento=event)
        return render(request, 'incidencia/nueva_incidencia.html', {'success': True,'eventos': eventos_list})
    else:
        return render(request, 'incidencia/nueva_incidencia.html', {"eventos": eventos_list})
