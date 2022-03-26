from django.shortcuts import render, redirect

# Create your views here.
from main.forms import RegisterClientForm


def registerClientView(request):
    if request.method == 'POST':
        form = RegisterClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterClientForm()
    return render(request, 'registerClient.html', {'form': form})
