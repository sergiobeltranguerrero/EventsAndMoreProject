from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import Assignacion
from .evento import State
from main.decorators import rols_required

def show_info_client(request):
    if not request.user.is_anonymous:
        if request.user.is_cliente:
            assignaciones = list()
            if request.method == 'GET':
                for id_assignacion in Assignacion.objects.filter(cliente_id=request.user.id):
                    assignaciones.append(id_assignacion)
                return render(request,'cliente/client.html',{'lista':assignaciones})
    else:
        return render(request,'error/404.html')


@rols_required(['personal_direccion'])
def client_facturation(request,id):
    states = []
    for estado in Assignacion.ESTADO:
        states.append(State(estado[0], estado[1]))
    states.pop(0)
    states.pop(0)
    assignacion =[assignaciones for assignaciones in Assignacion.objects.filter(estado='AP',evento_id=id) ]
    assignacion +=[assignaciones for assignaciones in Assignacion.objects.filter(estado='FD',evento_id=id) ]
    if request.method == 'POST':
        assign = Assignacion.objects.get(cliente_id=request.POST['Valor'][0], estado='AP',stand_id=request.POST['Valor'][1])
        assign.estado = 'FD'
        assign.save()
        assignacion = [assignaciones for assignaciones in Assignacion.objects.filter(estado='AP', evento_id=id)]
        assignacion += [assignaciones for assignaciones in Assignacion.objects.filter(estado='FD', evento_id=id)]

    return render(request,'evento/client_facturation.html',{'states' : states, 'assignacion' : assignacion, 'id' : id})