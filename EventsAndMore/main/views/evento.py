from django.shortcuts import render
from main.models import *
from datetime import datetime,date
from dateutil.relativedelta import relativedelta

def list_events(request):
    if request.method == 'GET':
        eventos = Evento.objects.filter(fecha_inicio__gt=datetime.now())
        json = set_dates()
    elif request.method == 'POST':
        json = get_dates(request=request)
        eventos = Evento.objects.filter(fecha_inicio__gt=json.get('date_start_start',json['mindate']),
                                        fecha_inicio__lt=json.get('date_start_end',json['maxdate']),
                                        fecha_fin__gt=json.get('date_end_start',json['mindate']),
                                        fecha_fin__lt=json.get('date_end_end',json['maxdate']))
    else:
        return render(request, '/')
    json['eventos'] = eventos
    return render(request, 'evento\list_event.html', json)

def detail_event(request,id):
    if request.method == 'GET':
        evento = Evento.objects.get(id=id)
        json = {'evento': evento}
        return render(request, 'evento\detail_event.html', json)
    if request.method == 'POST':
        return null

def set_dates(start_date=datetime.now(), end_date = datetime.now() + relativedelta(months=2)):
    mindate,maxdate = get_min_max_date()
    return {'mindate':mindate,'maxdate':maxdate,'date_start_start':start_date,
            'date_start_end':end_date,'date_end_start':start_date,'date_end_end':end_date}

def get_dates(request):
    date_names = ['date_start_start','date_start_end','date_end_start','date_end_end']
    mindate, maxdate = get_min_max_date()
    json = {'mindate':mindate,'maxdate':maxdate}
    for date_name in date_names:
        try:
            json[date_name] = get_str_to_date(request=request,str_date=date_name,format='%Y-%m-%d')
        except Exception as e:
            splt = date_name.split('_')
            if splt[(len(splt)-1)] == 'start':
                json[date_name] = json['mindate']
            else:
                json[date_name] = json['maxdate']
            next
    return json

def get_str_to_date(request,str_date,format):
    return datetime.strptime(request.POST[str_date], format).date()

def get_min_max_date():
    mindate = datetime.now() + relativedelta(months=-2)
    maxdate = datetime.now() + relativedelta(years=1)
    return mindate,maxdate