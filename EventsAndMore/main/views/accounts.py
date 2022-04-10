from django.shortcuts import render, redirect

# Create your views here.
from main.forms import RegisterClientForm
from main.models import Sector


def RegisterClientView(request):
    secotres = Sector.objects.all()
    if request.method == 'POST':
        form = RegisterClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterClientForm()
    return render(request, 'registration/registerClient.html', {'form': form, 'sectors': secotres})

