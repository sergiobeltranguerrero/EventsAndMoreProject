from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..models import Evento,Assignacion,Stand,Servicios_Asignados,Cliente, Servicio

@login_required
def show_info_client(request):
    assignaciones = list()
    if request.method == 'GET':
        for id_assignacion in Assignacion.objects.filter(cliente_id=request.user.id):
            assignaciones.append(id_assignacion)
        return render(request,'cliente/client.html',{'lista':assignaciones})
