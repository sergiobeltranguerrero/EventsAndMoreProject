from django.shortcuts import render
from main.models import *

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

def stand_planning_original(request,id_event):
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
        #ids=[]
        #for es in ess:
        #    ids.append(es.stand.id)
        ids = get_lst_from_query_set(ess.values('stand_id'),'stand_id')
        stand = Stand.objects.exclude(pk__in=ids)
        sector = Sector.objects.all()
        sizes = Evento_Stand_Sector.SIZE
        json = {'ess':ess,'stands':stand,'sectores':sector,'evento':evento,'sizes':sizes}
        return render(request,'evento\stand_planning_edit.html',json)
    elif request.method == 'POST':
        update_delete_ess(request,id_event)
        create_ess(request,id_event)
        return render(request, '/')
    else:
        return render(request, '/')

def stand_planning(request, id_event):
    evento = Evento.objects.get(id=id_event)
    if request.method == 'GET':
        if Evento_Stand_Sector.objects.filter(evento=evento).count() == 0:
            stand = Stand.objects.all()
            sector = Sector.objects.all()
            sizes = Evento_Stand_Sector.SIZE
            json = {'stands': stand, 'sectores': sector, 'evento': evento, 'sizes': sizes}
            return render(request, 'evento\stand_planning.html', json)
        else:
            return render(request, 'notAutorized.html')
    elif request.method == 'POST':
        if Evento_Stand_Sector.objects.filter(evento=evento).count() == 0:
            create_ess(request,id_event)
            return render(request, '/')
        else:
            return render(request, 'notAutorized.html')
    else:
        return render(request, '/')

def update_delete_ess(request,id_event):
    evento = Evento.objects.get(id=id_event)
    lstValues = []
    lstDeletes = []
    ess = Evento_Stand_Sector.objects.filter(evento=evento)
    ess_ids = get_lst_from_query_set(ess.model.objects.filter(evento=evento).values('id'),'id')
    lst_obj = get_elements_by_request_post(ess_ids, ['id', 'size', 'sector'], "delete", request)
    for obj in lst_obj:
        ess = Evento_Stand_Sector.objects.get(id=obj.__getattribute__('id'))
        try:
            lstDeletes.append(obj.__getattribute__('delete'))
        except:
            print('No delete on id: ' + str(obj.__getattribute__('id')))
        if not obj.__getattribute__('sector') == 'none':
            ess.sector = Sector.objects.get(id=obj.__getattribute__('sector'))
            ess.stand_size = obj.__getattribute__('size')
            lstValues.append(ess)
    Evento_Stand_Sector.objects.bulk_update(lstValues, ['stand_size', 'sector'])
    essd = Evento_Stand_Sector.objects.filter(pk__in=lstDeletes)
    essd.delete()

def create_ess(request,id_event):
    evento = Evento.objects.get(id=id_event)
    sids = get_lst_from_query_set(Evento_Stand_Sector.objects.filter(evento=evento).values('stand_id'),'stand_id')
    if sids.__len__() > 0:
        ids = get_lst_from_query_set(Stand.objects.exclude(pk__in=sids).values('id'),'id')
    else:
        ids = get_lst_from_query_set(Stand.objects.values('id'),'id')
    lst_values = []
    lst_elements = get_elements_by_request_post(ids,['id_stand','size','sector'],'',request)
    for element in lst_elements:
        stand = Stand.objects.get(id=element.__getattribute__('id_stand'))
        if not element.__getattribute__('sector') == 'none' and not element.__getattribute__('size') == '':
            sector = Sector.objects.get(id=element.__getattribute__('sector'))
            lst_values.append(Evento_Stand_Sector(stand=stand, sector=sector, evento_id=evento.id, stand_size=element.__getattribute__('size')))
    Evento_Stand_Sector.objects.bulk_create(lst_values)

def get_elements_by_request_post(lst_id,str_post_lst,try_post_elem,request):
    lst_obj = []
    for id in lst_id:
        obj = get_from_request_post(id,str_post_lst,try_post_elem,request)
        try:
            obj.__getattribute__(str_post_lst[0])
            lst_obj.append(obj)
        except:
            print('No exists id:'+str(id))
    return lst_obj

def get_from_request_post(id,str_post_lst,try_post_elem,request):
    class Dynamic:
        idess = ''
    dynamic = Dynamic()
    for element in str_post_lst:
        try:
            aux = request.POST[element+str(id)]
            dynamic.__setattr__(element, aux)
        except:
            print('For try attribute: ' + element + ' and id: ' + str(id) + ' no data found')
    try:
        tr_aux = request.POST[try_post_elem + str(id)]
        dynamic.__setattr__(try_post_elem, tr_aux)
    except:
        print('For try attribute: '+try_post_elem+' and id: '+str(id)+' element not found')
    return dynamic

def get_lst_from_query_set(query_set,name):
    elements = []
    for element in query_set:
        elements.append(element[name])
    return elements