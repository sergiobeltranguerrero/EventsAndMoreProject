'''2,621 65 47 10,55270866A,eventsandmore,calle españa,barcelona,barcelona,españa,930 20 27 90,events@hotmail.com,0,1,2
'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Assignacion, Cliente
from .evento import State


@login_required
def mostrar_assignaciones(request):
    assignaciones = Assignacion.objects.all()
    states = []
    for estado in Assignacion.ESTADO:
        states.append(State(estado[0], estado[1]))
    if request.method == 'POST':
        if not request.POST['state'] == '%':
            assignaciones = Assignacion.objects.filter(estado=request.POST['state'])
        else:
            assignaciones = Assignacion.objects.all()
    return render(request, "assignacion/assignaciones.html", {"assignaciones": assignaciones, 'states': states})


@login_required
def detalles_assignacion(request,id_assignacion):
    states = []
    for estado in Assignacion.ESTADO:
        states.append(State(estado[0], estado[1]))
    if request.method == 'POST':
        if request.POST['Valor'] == 'RC':
            assignaciones = Assignacion.objects.get(id=id_assignacion)
            assignaciones.estado = 'RC'
            assignaciones.save()
            assignaciones2 = Assignacion.objects.filter(id=id_assignacion)
            return render(request, "assignacion/detalles_assignacion.html",{"assignaciones": assignaciones2, 'cliente': assignaciones2[0].cliente,'comentario': assignaciones2[0].id, 'states': states})
        if request.POST['Valor'] == 'AP':
            assignaciones = Assignacion.objects.get(id=id_assignacion)
            assignaciones.estado = 'AP'
            assignaciones.save()
            assignaciones2 = Assignacion.objects.filter(id=id_assignacion)
            return render(request, "assignacion/detalles_assignacion.html",
                          {"assignaciones": assignaciones2, 'cliente': assignaciones2[0].cliente,
                           'comentario': assignaciones2[0].id, 'states': states})

        if request.POST['Valor'] == 'Comentario':
            assignaciones = Assignacion.objects.get(id=id_assignacion)
            assignaciones.comentario = str(request.POST['comentario'])
            assignaciones.save()
            assignaciones2 = Assignacion.objects.filter(id=id_assignacion)
            return render(request, "assignacion/detalles_assignacion.html", {"assignaciones": assignaciones2, 'cliente' : assignaciones2[0].cliente,'comentario' : assignaciones2[0].id,'states': states})
        if request.POST['Valor'] == 'Return':
            assignaciones = Assignacion.objects.all()
            return render(request, "assignacion/assignaciones.html", {"assignaciones": assignaciones, 'states': states})


    else:
        assignaciones = Assignacion.objects.filter(id=id_assignacion)
        return render(request, "assignacion/detalles_assignacion.html", {"assignaciones": assignaciones, 'cliente' : assignaciones[0].cliente,'comentario' : assignaciones[0].id,'states': states})

