from django.shortcuts import render

from main.models import Servicio

def listServices(request):
    services = Servicio.objects.all()
    return render(request,"servicios/listService.html",{"servicios":services})
