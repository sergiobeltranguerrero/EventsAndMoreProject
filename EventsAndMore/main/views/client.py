from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models.servicios import Assignacion

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