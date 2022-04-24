# this lets the user create an incidence
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Incidencia, Cliente
from .evento import State



@login_required
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
    if request.method == 'POST':
        if request.POST['Valor'] == 'Return':
            cliente = Cliente.objects.get(user=request.user)
            incidencia = Incidencia.objects.filter(cliente_id=cliente.id)
            return render(request, "incidencia/incidencia.html", {"incidencia": incidencia, 'states': states})
    else:
        cliente = Cliente.objects.get(user=request.user)
        incidencia = Incidencia.objects.filter(id = id_incidencia)
        incidencia2 = Incidencia.objects.get(id = id_incidencia)
        if request.user.id == incidencia2.cliente.user.id:
            if not incidencia2.estadoIn == 'SC':
                return render(request,"incidencia/detalles_incidencia.html",{"indicencia" : incidencia, 'id' : incidencia[0].id, "cliente" : cliente, 'states': states, "descripcion" : incidencia[0].descripcion})
            else:
                incidencia = Incidencia.objects.filter(cliente_id=cliente.id)
                return render(request, "incidencia/incidencia.html", {"incidencia": incidencia, 'states': states})
        else:
            return render(request, "home.html")




@login_required
def NuevaIncidencia(request):

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        cliente = Cliente.objects.get(user=request.user)
        Incidencia.objects.create(nombre=nombre, descripcion=descripcion,estadoIn='PD', cliente=cliente, gestion_id=1)
        return render(request, 'incidencia/nueva_incidencia.html')
    else:
        return render(request, 'incidencia/nueva_incidencia.html')

