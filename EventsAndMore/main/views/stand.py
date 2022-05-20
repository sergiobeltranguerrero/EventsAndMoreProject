from django.shortcuts import render
from main.models import *
from django.contrib.auth.decorators import login_required
from .evento import my_events
from main.decorators import organizador_eventos_only, cliente_only

error_title = 'Esta pagina no existe o no tiene los permisos necessarios'
error_description = 'Esta intentando acceder a una pagina inexistente o usted no tiene permisos para acceder'

#GET: Gets stands for the client sector and one event
#POST: Creates new assignations for a event and client sector by selected by the user
@login_required
@cliente_only
def get_stands_by_sector_event(request, id_event):
    evento = Evento.objects.get(id=id_event)
    cliente = Cliente.objects.get(user=request.user)
    stands_id = []
    eas = Evento_Stand_Sector.objects.filter(evento=evento, sector=cliente.sector)
    for stand in eas:
        stands_id.append(stand.stand.id)
    if request.method == 'GET':
        assignados = Assignacion.objects.filter(evento=evento,stand_id__in=stands_id)
        for ea in eas:
            if assignados.filter(stand_id=ea.stand_id).exists():
                eas = eas.exclude(stand_id=ea.stand_id)
        json = {'eas':eas,'assignados':assignados, 'evento':evento}
        return render(request,'stand\get_stand.html',json)
    elif request.method == 'POST':
        lst_obj = get_elements_by_request_post(stands_id, ['id', 'size', 'sector'], 'selected', request)
        assignaciones = []
        for obj in lst_obj:
            try:
                if obj.__getattribute__('selected') == 'true':
                    assignaciones.append(Assignacion(evento=evento,cliente=cliente,stand_id=obj.__getattribute__('id'),estado='PD'))
            except:
                next
        if len(assignaciones) > 0:
            Assignacion.objects.bulk_create(assignaciones)
        request.method = 'GET'
        return my_events(request)
    else:
        return render(request, "error/error_generico.html",
                      {'error': {'title': error_title, 'message': error_description}})


@login_required
@organizador_eventos_only
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
        return render(request, 'home.html')
    else:
        return render(request, "error/error_generico.html",
                      {'error': {'title': error_title, 'message': error_description}})


@login_required
@organizador_eventos_only
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
            return render(request, "error/error_generico.html",
                          {'error': {'title': error_title, 'message': error_description}})
    elif request.method == 'POST':
        if Evento_Stand_Sector.objects.filter(evento=evento).count() == 0:
            create_ess(request,id_event)
            return render(request, 'home.html')
        else:
            return render(request, "error/error_generico.html",
                          {'error': {'title': error_title, 'message': error_description}})
    else:
        return render(request, "error/error_generico.html",
                          {'error': {'title': error_title, 'message': error_description}})


@login_required
@cliente_only
def my_stand(request,id_event):
    states = []
    for estado in Assignacion.ESTADO:
        states.append(State(estado[0], estado[1]))
    cliente = Cliente.objects.get(user=request.user)
    assignaciones = Assignacion.objects.filter(cliente=cliente, evento_id=id_event)
    if request.method == 'POST':
        ass_id = []
        for ass in assignaciones:
            ass_id.append(ass.id)
        lst_obj = get_elements_by_request_post(ass_id, ['id'], 'delete', request)
        ass_id.clear()
        for obj in lst_obj:
            try:
                if obj.__getattribute__('delete') == 'true':
                    ass_id.append(obj.__getattribute__('id'))
            except:
                next
        assignaciones.filter(pk__in=ass_id).delete()
    assignaciones = Assignacion.objects.filter(cliente=cliente, evento_id=id_event)
    if not assignaciones.count() == 0:
        json = {'assignaciones': assignaciones, 'evento': assignaciones[0].evento, 'states': states}
        return render(request, 'stand/my_stand.html', json)
    else:
        return render(request, 'home.html')


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
            lst_values.append(Evento_Stand_Sector(stand=stand, sector=sector, evento_id=evento.id,
                                                  stand_size=element.__getattribute__('size')))
    Evento_Stand_Sector.objects.bulk_create(lst_values)


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
        z=''
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


class State:
    id = ''
    name = ''

    def __init__(self,id,name):
        self.id = id
        self.name = name
