from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from main.forms import RegisterClientForm
from .models import *

def RegisterClientView(request):
    if request.method == 'POST':
        form = RegisterClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterClientForm()
    return render(request, 'registerClient.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class AdminView(TemplateView):
    template_name = 'admin.html'


def stand_planning(request,id_event):
    if request.method == 'GET':
        evento = Evento.objects.get(id=id_event)
        stand = Stand.objects.all()
        sector = Sector.objects.all()
        json = {'stands':stand,'sectores':sector,'evento':evento}
        return render(request,'evento\stand_planning.html',json)
    elif request.method == 'POST':
        lstValues = []
        for id in [1,Stand.objects.count()]:
            id_stand = request.POST["idStand"+id]
            size = request.POST["size"+id]
            sector = request.POST["id_sector"]

        valor = Evento_Stand_Sector()
        return render(request, 'evento\stand_planning.html')
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