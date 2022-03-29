from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from main.forms import RegisterClientForm
from .models import *
import viewsEvento


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
