'''2,621 65 47 10,55270866A,eventsandmore,calle españa,barcelona,barcelona,españa,930 20 27 90,events@hotmail.com,0,1,2
'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Assignacion, Cliente


@login_required
def mostrar_assignaciones(request):
    if request.method == 'GET':
        assignaciones = Assignacion.objects.all()
        return render(request, "assignaciones.html", {"assignaciones": assignaciones})





#def listStock(request):
#   productes = Stock.objects.filter(floristeria=request.user.floristeria)
#  return render(request, "Stock/list.html", {"productes": productes})
