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

@rols_required(['personal_direccion'])
def show_events_facturation(request,id):
    eventos =[]
    assignaciones=Assignacion.objects.all().order_by('evento_id')
    for ass in assignaciones:
        if eventos.count() == 0:
            eventos.append(Evento_f(evento=ass.evento,estado=ass.estado))
        else:
            modifyed = False
            for evento in eventos:
                if ass.evento.id == evento.evento.id:
                    evento.estados.append(ass.estado)
                    modifyed = True
                    break
            if not modifyed:
                eventos.append(Evento_f(evento=ass.evento, estado=ass.estado))
    for evento in eventos:
        evento.setEstado()
    return render(request, 'evento/facturation_eventos.html', {'eventos': eventos})



@rols_required(['personal_direccion'])
def show_event_facturation(request, id):
    assignaciones = Assignacion.objects.filter(evento_id=id)
    evento = assignaciones.first().evento
    clientes = []
    for ass in assignaciones:
        if eventos.count() == 0:
            clientes.append(Evento_f(evento=ass.cliente,estado=ass.estado))
        else:
            modifyed = False
            for cliente in clientes:
                if ass.cliente.id == cliente.evento.id:
                    cliente.estados.append(ass.estado)
                    modifyed = True
                    break
            if not modifyed:
                eventos.append(Evento_f(evento=ass.cliente, estado=ass.estado))
    for cliente in clientes:
        cliente.setEstado()
    return render(request, 'evento/facturation_evento.html', {'evento': evento,'clientes': clientes})

class Evento_f:
    evento = ''
    estado = ''
    estados = []
    delete = False

    def __init__(self, evento,estado):
        self.evento = evento
        self.estados.append(estado)

    def setEstado(self):
        state = 'Pendiente'
        for state in estados:
            if state == 'PD':
                delete = True
                break
            elif param == 'RC':
                delete = True
                break
            elif param == 'AP':
                break
            elif param == 'FD':
                estado = 'Facturado'

