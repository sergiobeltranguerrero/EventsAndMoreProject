from django.shortcuts import render
from main.models import *
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required

error_title = 'Esta pagina no existe o no tiene los permisos necessarios'
error_description = 'Esta intentando acceder a una pagina inexistente o usted no tiene permisos para acceder'

# Shows all events in current year
def list_events(request):
    if request.method == 'GET':
        eventos = Evento.objects.filter(fecha_inicio__gt=datetime.now())
        json = set_dates()
    elif request.method == 'POST':
        json = get_dates(request=request)
        eventos = Evento.objects.filter(fecha_inicio__range=(json.get('date_start', json['mindate']),json.get('date_end', json['maxdate'])))
    else:
        return render(request, '/')
    if not request.user.is_anonymous and request.user.is_cliente:
        ids2 = Evento_Stand_Sector.objects.filter(sector=request.user.cliente.sector).values('evento_id').order_by(
            'evento_id')
        ids = ids2.distinct()
        eventos = eventos.filter(pk__in=ids)
    json['eventos'] = eventos
    return render(request, 'evento/list_event.html', json)


# Shows an specific event passed by paramether
def detail_event(request, id):
    if request.method == 'GET':
        evento = Evento.objects.get(id=id)
        json = {'evento': evento}
        return render(request, 'evento/detail_event.html', json)
    if request.method == 'POST':
        return render(request, "error/error_generico.html", {'error': {'title': error_title,'message': error_description}})


# Shows events that user have solicitated
@login_required
def my_events(request):
    states = []
    for estado in Assignacion.ESTADO:
        states.append(State(estado[0], estado[1]))
    cliente = Cliente.objects.get(user=request.user)
    if request.method == 'GET':
        assignaciones = Assignacion.objects.filter(cliente=cliente)
    elif request.method == 'POST':
        if not request.POST['state'] == '%':
            assignaciones = Assignacion.objects.filter(cliente=cliente, estado=request.POST['state'])
        else:
            assignaciones = Assignacion.objects.filter(cliente=cliente)
    else:
        return render(request, "error/error_generico.html", {'error': {'title': error_title,'message': error_description}})
    asss = create_Ass(assignaciones)
    json = {'customs': asss, 'states': states}
    if request.method == 'GET':
        json['selection'] = ''
    else:
        json['selection'] = request.POST['state']
    return render(request, 'evento/my_events.html', json)


def create_Ass(assiganciones):
    ass = []
    for asig in assiganciones:
        if len(ass) == 0:
            ass.append(new_Ass(asig))
        else:
            exist = False
            for as_ in ass:
                if as_.event_id == asig.evento.id:
                    exist = True
                    as_.lst_ass_stand += ', ' + str(asig.stand.numero_stand)
                    break
            if not exist:
                ass.append(new_Ass(asig))
    return ass


def new_Ass(asig):
    state = ''
    for estate in asig.ESTADO:
        if estate[0] == asig.estado:
            state = State(estate[0], estate[1])
            break
    return Ass(lst_ass_stand=str(asig.stand.numero_stand), event_id=asig.evento_id,
               event_name=asig.evento.nombre, event_description=asig.evento.descripcion,
               start_date=asig.evento.fecha_inicio, end_date=asig.evento.fecha_fin,
               capacity=asig.evento.capacidad, state=state,
               comentary='')


def set_dates(start_date=datetime.now(), end_date=datetime.now() + relativedelta(months=2)):
    mindate, maxdate = get_min_max_date()
    return {'mindate': mindate, 'maxdate': maxdate, 'date_start_start': start_date,
            'date_start_end': end_date, 'date_end_start': start_date, 'date_end_end': end_date}


def get_dates(request):
    date_names = ['date_start', 'date_end']
    mindate, maxdate = get_min_max_date()
    json = {'mindate': mindate, 'maxdate': maxdate}
    for date_name in date_names:
        try:
            json[date_name] = get_str_to_date(request=request, str_date=date_name, format='%Y-%m-%d')
        except Exception as e:
            splt = date_name.split('_')
            if splt[(len(splt) - 1)] == 'start':
                json[date_name] = json['mindate']
            else:
                json[date_name] = json['maxdate']
            next
    return json


def get_str_to_date(request, str_date, format):
    return datetime.strptime(request.POST[str_date], format).date()


def get_min_max_date():
    mindate = datetime.now() + relativedelta(months=-2)
    maxdate = datetime.now() + relativedelta(years=1)
    return mindate, maxdate


class Ass:
    lst_ass_stand = ''
    event_id = 0
    event_name = ''
    event_description = ''
    start_date = ''
    end_date = ''
    capacity = 0
    state = ''
    comentary = ''

    def __init__(self, lst_ass_stand, event_id, event_name, event_description, start_date, end_date, capacity, state,
                 comentary):
        self.lst_ass_stand = lst_ass_stand
        self.event_id = event_id
        self.event_name = event_name
        self.event_description = event_description
        self.start_date = start_date
        self.end_date = end_date
        self.capacity = capacity
        self.state = state
        self.comentary = comentary


class State:
    id = ''
    name = ''

    def __init__(self, id, name):
        self.id = id
        self.name = name
