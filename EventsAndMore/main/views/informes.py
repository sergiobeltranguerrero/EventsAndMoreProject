import datetime
import json
import locale

from django.http import JsonResponse
from django.shortcuts import render

from main.models import Evento, Assignacion, Orden_Servicios, Servicios_Orden


def informe_mensual_eventos(request):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    eventos = Evento.objects.all().order_by('fecha_inicio')
    if request.method == 'GET':
        # Obtenemos el mes y el año de los eventos
        meses = set()
        for evento in eventos:
            meses.add(str(evento.fecha_inicio.strftime('%B')) + '-' + str(evento.fecha_inicio.year))
        return render(request, 'informes/informe_mensual.html', {'meses': meses})

    if request.method == 'POST':
        mes = request.POST['mes']
        mes = mes.split('-')
        datetime_object = datetime.datetime.strptime(mes[0], "%B")
        month_number = datetime_object.month
        eventos_mes = Evento.objects.filter(fecha_inicio__month=month_number, fecha_inicio__year=mes[1])
        num_eventos = len(eventos_mes)
        asignaciones = Assignacion.objects.filter(evento__in=eventos_mes, estado='AP')
        num_asignaciones = len(asignaciones)
        clients_in_events = get_clients_in_events(eventos_mes)
        num_servicios = get_num_servicies(eventos_mes)

        return render(request, 'informes/info.html',
                      {'eventos': eventos_mes, 'num_eventos': num_eventos, 'num_asignaciones': num_asignaciones,
                       'clients_in_events': clients_in_events, 'num_servicios': num_servicios,
                       "num_servicios_desglosado": get_all_services_in_events(eventos_mes), 'mes': mes[0]})

    return render(request, 'informes/informe_mensual.html')


def get_clients_in_events(events):
    clients = dict()
    for event in events:
        asignaciones = Assignacion.objects.filter(evento=event, estado='AP')
        clients[str(event)] = len(asignaciones)
    return clients


def get_num_servicies(events):
    num_servicies = 0
    for event in events:
        orden = Orden_Servicios.objects.filter(evento=event)
        if orden:
            servicios = Servicios_Orden.objects.filter(orden=orden)
            for servicio in servicios:
                num_servicies += servicio.cantidad
    return num_servicies


def get_all_services_in_events(events):
    services = dict()
    for event in events:
        orden = Orden_Servicios.objects.filter(evento=event)
        if orden:
            servicios = Servicios_Orden.objects.filter(orden=orden)
            for servicio in servicios:
                if servicio.servicio.nombre not in services:
                    services[servicio.servicio.nombre] = servicio.cantidad
                else:
                    services[servicio.servicio.nombre] += servicio.cantidad
    return services
