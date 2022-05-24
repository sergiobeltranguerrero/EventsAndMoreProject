# this lets the user create an incidence
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..models import Incidencia, Cliente, Evento, Assignacion, Servicios_adicionales, Comentario
from .evento import State
from ..decorators import servicios_adiciones_and_cliente, servicios_adicionales, rols_required
from django.urls import reverse


@servicios_adiciones_and_cliente
def Incidencias(request):
    user = request.user
    states = []
    for estado in Incidencia.ESTADO:
        states.append(State(estado[0], estado[1]))

    if request.method == 'POST':
        if request.user.is_servicios_adicionales:
            adicionales = Servicios_adicionales.objects.get(user_id=request.user.id)
            if not request.POST['state'] == '%':
                incidencia = Incidencia.objects.filter(estadoIn=request.POST['state'], gestion=adicionales)
            else:
                incidencia = [incidencia for incidencia in Incidencia.objects.filter(estadoIn='PD')]
                incidencia += [incidencia for incidencia in Incidencia.objects.filter(estadoIn='EP', gestion=adicionales)]
                incidencia += [incidencia for incidencia in Incidencia.objects.filter(estadoIn='SC', gestion=adicionales)]


        elif request.user.is_cliente:
            if not request.POST['state'] == '%':
                cliente = Cliente.objects.get(user=request.user)
                incidencia = Incidencia.objects.filter(estadoIn=request.POST['state'], cliente_id=cliente.id)
            else:
                cliente = Cliente.objects.get(user=request.user)
                incidencia = Incidencia.objects.filter(cliente_id=cliente.id)

        return render(request, "incidencia/incidencia.html", {"incidencia": incidencia, 'states': states, 'user': user})

    if request.method == 'GET':
        if request.user.is_servicios_adicionales:
            adicionales = Servicios_adicionales.objects.get(user_id=request.user.id)
            incidencia = [incidencia for incidencia in Incidencia.objects.filter(estadoIn='PD')]
            incidencia += [incidencia for incidencia in Incidencia.objects.filter(estadoIn='EP', gestion=adicionales)]
            incidencia += [incidencia for incidencia in Incidencia.objects.filter(estadoIn='SC', gestion=adicionales)]


        elif request.user.is_cliente:
            cliente = Cliente.objects.get(user=request.user)
            incidencia = [incidencia for incidencia in Incidencia.objects.filter(estadoIn='PD', cliente_id=cliente.id)]
            incidencia += [incidencia for incidencia in Incidencia.objects.filter(estadoIn='EP', cliente_id=cliente.id)]
            incidencia += [incidencia for incidencia in Incidencia.objects.filter(estadoIn='SC', cliente_id=cliente.id)]
        return render(request, "incidencia/incidencia.html", {"incidencia": incidencia, 'states': states, 'user': user})


@rols_required('cliente')
def detalles_incidencia(request, id_incidencia):
    states = []
    for estado in Incidencia.ESTADO:
        states.append(State(estado[0], estado[1]))

        cliente = Cliente.objects.get(user=request.user)
        incidencia = Incidencia.objects.filter(id=id_incidencia)
        try:
            incidencia2 = Incidencia.objects.get(id=id_incidencia)
        except:
            return render(request, "error/error_generico.html", {'error': {
                'title': 'Esta pagina no existe',
                'message': 'O usted no tiene los permisos necesarios'
            }})
        if request.user.id == incidencia2.cliente.user.id:
            if not incidencia2.estadoIn == 'SC':
                return render(request, "incidencia/detalles_incidencia.html",
                              {"indicencia": incidencia, 'id': incidencia[0].id, "cliente": cliente, 'states': states,
                               "descripcion": incidencia[0].descripcion})
            else:
               comentario = Comentario.objects.get(incidencia_id=id_incidencia)
               return render(request, "incidencia/detalles_incidencia.html",
                             {"indicencia": incidencia,'inci': incidencia[0], 'id': incidencia[0].id, "cliente": cliente, 'states': states,
                              "descripcion": incidencia[0].descripcion, 'comentario': comentario})
        else:
            return render(request, "error/error_generico.html", {'error': {
                'title': 'Esta pagina no existe',
                'message': 'O usted no tiene los permisos necesarios'
            }})


@rols_required('cliente')
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
        Incidencia.objects.create(nombre=nombre, descripcion=descripcion, estadoIn='PD', cliente=cliente, gestion_id=1,
                                  evento=event)
        return render(request, 'incidencia/nueva_incidencia.html', {'success': True, 'eventos': eventos_list})
    else:
        return render(request, 'incidencia/nueva_incidencia.html', {"eventos": eventos_list})


@servicios_adicionales
def valorar_incidencia(request, id_incidencia):
    states = []
    for estado in Incidencia.ESTADO:
        states.append(State(estado[0], estado[1]))
    if request.method == 'GET':
        incidencia = Incidencia.objects.filter(id=id_incidencia)
        if len(incidencia) > 0 and incidencia[0].estadoIn == 'SC':
            comentario = Comentario.objects.get(incidencia_id=id_incidencia)
            return render(request, "incidencia/valorar_incidencia.html",
                          {"incidencias": incidencia, 'cliente': incidencia[0].cliente, 'comentario': incidencia[0].id,
                           'states': states, "incidencia": incidencia[0], 'comentarios': comentario})
        try:
            return render(request, "incidencia/valorar_incidencia.html",
                          {"incidencias": incidencia, 'cliente': incidencia[0].cliente, 'comentario': incidencia[0].id,
                           'states': states, "incidencia": incidencia[0]})
        except:
            return render(request, "error/error_generico.html", {'error': {
                'title': 'Esta pagina no existe',
                'message': 'O usted no tiene los permisos necesarios'
            }})

    if request.method == 'POST':
        if request.POST['Valor'] == 'asignar':
            incidencia = Incidencia.objects.get(id=id_incidencia)
            incidencia.estadoIn = 'EP'
            adicionales = Servicios_adicionales.objects.get(user_id=request.user.id)
            incidencia.gestion = adicionales
            incidencia.save()
            incidencia = Incidencia.objects.filter(id=id_incidencia)
            return render(request, "incidencia/valorar_incidencia.html",
                          {"incidencias": incidencia, 'cliente': incidencia[0].cliente, 'comentario': incidencia[0].id,
                           'states': states})

        elif request.POST['Valor'] == 'solucionada' and len(request.POST['asunto']) >= 5:
            incidencia = Incidencia.objects.get(id=id_incidencia)
            incidencia.estadoIn = 'SC'
            incidencia.descripcion = str(request.POST['comentario'])
            incidencia.save()
            # incidencia.descripcion = str(request.POST['comentario'])
            try:
                Comentario.objects.create(asunto=request.POST['asunto'], cuerpo=request.POST['comentario'],
                                          incidencia_id=id_incidencia)
            except:
                comentario = Comentario.objects.get(incidencia_id=id_incidencia)
                comentario.asunto = str(request.POST['asunto'])
                comentario.cuerpo = str(request.POST['comentario'])
                comentario.save()
            recipientes = []
            recipientes.append(incidencia.cliente.user.email)
            recipientes.append(request.user.email)
            send_mail('Incidencia solucionada!', 'Titulo de la incidencia: ' + incidencia.nombre + '\nDescripción de '
                                                                                                   'la incidencia: '
                      + incidencia.descripcion + '\nEsta incidencia ha sido solucionada, esperemos que haya visto '
                                                 'adecuada la respuesta a su incidencia.' + '\nMuchas gracias'
                      + '\n\n' + request.user.first_name + ' ' + request.user.last_name, 'eventsandmore@correo.com',
                      recipientes, fail_silently=False)

            incidencia = Incidencia.objects.filter(id=id_incidencia)
            return render(request, "incidencia/valorar_incidencia.html",
                          {"incidencias": incidencia, 'cliente': incidencia[0].cliente, 'comentario': incidencia[0].id,
                           'states': states})
        elif request.POST['Valor'] == 'desasignar':
            incidencia = Incidencia.objects.get(id=id_incidencia)
            incidencia.estadoIn = 'PD'
            incidencia.save()
            incidencia = Incidencia.objects.filter(id=id_incidencia)
            return render(request, "incidencia/valorar_incidencia.html",
                          {"incidencias": incidencia, 'cliente': incidencia[0].cliente, 'comentario': incidencia[0].id,
                           'states': states})


