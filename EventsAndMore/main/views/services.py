from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

#Create viw here
from EventsAndMore.main.models import Servicio

#@login_required
def ListServices(request):
    services = Servicio.objects.all()
    return render(request, "Services/list_service.html", {"servicios":services})