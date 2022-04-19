# this lets the user create an incidence
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Incidencia, Cliente



@login_required
def Incidencias(request):

    if request.method == 'GET':
        cliente = Cliente.objects.get(user=request.user)
        incidencia = Incidencia.objects.filter(cliente_id =cliente.id)
        return render(request, "incidencia.html", {"incidencia": incidencia})




@login_required
def NuevaIncidencia(request):

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        cliente = Cliente.objects.get(user=request.user)
        Incidencia.objects.create(nombre=nombre, descripcion=descripcion, cliente=cliente)
        return render(request,'nuevaincidencia.html')
    else:
        return render(request, 'nuevaincidencia.html')

