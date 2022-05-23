'''2,621 65 47 10,55270866A,eventsandmore,calle españa,barcelona,barcelona,españa,930 20 27 90,events@hotmail.com,0,1,2
'''
import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Assignacion, Cliente, Evento, Gestor_solicitudes
from .evento import State
from django.core.mail import send_mail
from main.decorators import gestor_solicitudes_and_cliente,rols_required

error_title = 'Esta pagina no existe o no tiene los permisos necessarios'
error_description = 'Esta intentando acceder a una pagina inexistente o usted no tiene permisos para acceder'

@gestor_solicitudes_and_cliente
def mostrar_assignaciones(request):
    states = []
    for estado in Assignacion.ESTADO:
        states.append(State(estado[0], estado[1]))
    if request.user.is_gestor_solicitudes:
        user = request.user
        assignaciones = [assignaciones for assignaciones in Assignacion.objects.filter(estado='PD')]
        assignaciones += [assignaciones for assignaciones in Assignacion.objects.filter(estado='AP')]
        assignaciones += [assignaciones for assignaciones in Assignacion.objects.filter(estado='RC')]
        if request.method == 'POST':
            if not request.POST['state'] == '%':
                assignaciones = Assignacion.objects.filter(estado=request.POST['state'])
            else:
                assignaciones = [assignaciones for assignaciones in Assignacion.objects.filter(estado='PD')]
                assignaciones += [assignaciones for assignaciones in Assignacion.objects.filter(estado='AP')]
                assignaciones += [assignaciones for assignaciones in Assignacion.objects.filter(estado='RC')]

        return render(request, "assignacion/assignaciones.html", {"assignaciones": assignaciones, 'states': states, 'user' : user})

    elif request.user.is_cliente:
        cliente = Cliente.objects.get(user = request.user)
        user = request.user
        assignaciones = Assignacion.objects.filter(cliente_id=cliente.id)

        if request.method == 'POST':
            if not request.POST['state'] == '%':
                assignaciones = Assignacion.objects.filter(estado=request.POST['state'], cliente_id=cliente.id)
            else:
                assignaciones = Assignacion.objects.filter(cliente_id=cliente.id)
        return render(request, "assignacion/assignaciones.html", {"assignaciones": assignaciones, 'states': states, 'user' : user})

def detalles_assignacion(request,id_assignacion):
    states = []
    for estado in Assignacion.ESTADO:
        states.append(State(estado[0], estado[1]))
    if request.method == 'POST':
        if request.POST['Valor'] == 'RC':
            assignaciones = Assignacion.objects.get(id=id_assignacion)
            assignaciones.estado = 'RC'
            assignaciones.es_valido_por_gestor = False
            assignaciones.save()
            assignaciones2 = Assignacion.objects.filter(id=id_assignacion)
            return render(request, "assignacion/detalles_assignacion.html",{"assignaciones": assignaciones2, 'cliente': assignaciones2[0].cliente,'comentario': assignaciones2[0].id, 'states': states})
        if request.POST['Valor'] == 'AP':
            assignaciones = Assignacion.objects.get(id=id_assignacion)
            assignaciones.estado = 'AP'
            assignaciones.es_valido_por_gestor = True
            assignaciones.save()
            assignaciones2 = Assignacion.objects.filter(id=id_assignacion)
            return render(request, "assignacion/detalles_assignacion.html",
                          {"assignaciones": assignaciones2, 'cliente': assignaciones2[0].cliente,
                           'comentario': assignaciones2[0].id, 'states': states})

        if request.POST['Valor'] == 'Comentario':

            assignaciones = Assignacion.objects.get(id=id_assignacion)
            if len(request.POST['comentario'])>=10:
                assignaciones.comentario = str(request.POST['comentario'])
                assignaciones.save()
            if not assignaciones.estado == 'PD':
                recipientes = []
                recipientes.append(assignaciones.cliente.user.email)
                recipientes.append(request.user.email)
                estado = assignaciones.estado
                if estado == 'AP':
                    estado = 'Aprovado'
                elif estado == 'RC':
                    estado = 'Rechazado'
                send_mail('Respuesta final de la solicitud',
                          'Evento de la asignacion: ' + assignaciones.evento.nombre + '\nNumero de stand deseado: ' + str(
                              assignaciones.stand.numero_stand) + '\nComentario de la assignación: ' + assignaciones.comentario + '\nEstado final de la assignación: ' + estado,
                          'eventsandmore@correo.com', recipientes, fail_silently=False)
            assignaciones2 = Assignacion.objects.filter(id=id_assignacion)
            return render(request, "assignacion/detalles_assignacion.html", {"assignaciones": assignaciones2, 'cliente' : assignaciones2[0].cliente,'comentario' : assignaciones2[0].id,'states': states})


    else:
        assignaciones = Assignacion.objects.filter(id=id_assignacion)
        try:
            return render(request, "assignacion/detalles_assignacion.html", {"assignaciones": assignaciones, 'cliente' : assignaciones[0].cliente,'comentario' : assignaciones[0].id,'states': states})
        except:
            return render(request, "error/error_generico.html", {'error': {
                'title': 'Esta pagina no existe',
                'message': 'O usted no tiene los permisos necesarios'
            }})

@rols_required(['gestor_solicitudes'])
def solicitudes_eventos(request):
    if request.method == 'POST':
        try:
            id = int(request.POST['id'])
            gestor = Gestor_solicitudes.objects.get(user=request.user)
            evento = Evento.objects.get(pk=id)
            evento.Validado_gestor = True
            evento.gestor_validador = gestor
            evento.save()
        except:
            return render(request, "error/error_generico.html",
                          {'error': {'title': error_title, 'message': error_description}})
    eventos = Evento.objects.filter(Validado_gestor=False, fecha_fin__gt=datetime.datetime.now())
    json = {'eventos': eventos}
    return render(request,'evento/solicitud_evento.html',json)