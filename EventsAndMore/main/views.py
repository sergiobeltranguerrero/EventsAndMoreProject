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


def stand_planning(request):
    if request.method == 'GET':
        stand = Stand.objects.all()
        sector = Sector.objects.all()
        json = {'stands':stand,'sectores':sector}
        return render(request,'evento\stand_planning.html',json)
    elif request.method == 'POST':
        return render(request, 'evento\stand_planning.html')
    else:
        return render(request, '/')