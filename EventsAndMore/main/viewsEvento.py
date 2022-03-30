from django.shortcuts import render, redirect
from .models import *


def setPlanningStand(request):
    stand = Stand.objects.all()
    sector = Sector.objects.all()
    json = {'stands':stand,'sectores':sector}
    return render(request,'evento\setStandSector.html',json)