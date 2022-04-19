# this lets the user create an incidence
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import *



@login_required
def Incidencias(request):
    if request.method == 'GET':



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

