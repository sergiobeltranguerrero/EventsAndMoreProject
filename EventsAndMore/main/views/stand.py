from django.shortcuts import render
from main.models import *

def stand_planning(request,id_event):
    evento = Evento.objects.get(id=id_event)
    if request.method == 'GET':
        stand = Stand.objects.all()
        sector = Sector.objects.all()
        sizes = Evento_Stand_Sector.SIZE
        json = {'stands':stand,'sectores':sector,'evento':evento,'sizes':sizes}
        return render(request,'evento\stand_planning.html',json)
    elif request.method == 'POST':
        lstValues = []
        for id in range(1,Stand.objects.count()+1):
            id_stand = request.POST["id_stand"+str(id)]
            stand = Stand.objects.get(id=id_stand)
            size = request.POST["size"+str(id)]
            id_sector = request.POST["sector"+ str(id)]
            if not id_sector == 'none' and not size == '':
                sector = Sector.objects.get(id=id_sector)
                lstValues.append(Evento_Stand_Sector(stand=stand,sector=sector,evento_id=evento.id,stand_size=size))
        Evento_Stand_Sector.objects.bulk_create(lstValues)
        return render(request, '/')
    else:
        return render(request, '/')

def stand_planning_edit(request,id_event):
    evento = Evento.objects.get(id=id_event)
    if request.method == 'GET':
        ess = Evento_Stand_Sector.objects.filter(evento=evento)
        ids=[]
        for es in ess:
            ids.append(es.stand.id)
        stand = Stand.objects.filter(pk__in=ids)
        sector = Sector.objects.all()
        sizes = Evento_Stand_Sector.SIZE
        json = {'ess':ess,'stands':stand,'sectores':sector,'evento':evento,'sizes':sizes}
        return render(request,'evento\stand_planning_edit.html',json)
    elif request.method == 'POST':
        lstValues = []
        for id in range(1,Stand.objects.count()+1):
            id_stand = request.POST["id_stand"+str(id)]
            stand = Stand.objects.get(id=id_stand)
            size = request.POST["size"+str(id)]
            id_sector = request.POST["sector"+ str(id)]
            if not id_sector == 'none' and not size == '':
                sector = Sector.objects.get(id=id_sector)
                lstValues.append(Evento_Stand_Sector(stand=stand,sector=sector,evento_id=evento.id,stand_size=size))
        Evento_Stand_Sector.objects.bulk_create(lstValues)
        return render(request, '/')
    else:
        return render(request, '/')


def get_stand(request,id_event):
    if request.method == 'GET':
        evento = Evento.objects.get(id=id_event)
        cliente = Cliente.objects.get(user=request.user)
        stand = Evento_Stand_Sector.objects.filter(evento=evento,sector=cliente.sector).model.stand
        assignados = Assignacion.objects.get(evento=evento,stand__in=stand.all())
        json = {'stands':stand,'assignados':assignados}
        return render(request,'stand\get_stand.html',json)
    elif request.method == 'POST':
        return render(request, 'stand\get_stand.html')
    else:
        return render(request, '/')