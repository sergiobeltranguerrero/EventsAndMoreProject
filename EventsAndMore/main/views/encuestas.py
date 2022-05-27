from __future__ import print_function

from datetime import datetime

from django.shortcuts import render

from EventsAndMore.settings import base as settings
from main.decorators import rols_required
from main.models import Encuesta, Evento
from main.utils.survey_monkey_api import SurveyMonkeyAPI


@rols_required(['personal_direccion', 'servicios_adicionales'])
def encuestas_creadas(request):
    """
    Vista para mostrar las encuestas creadas por el personal de dirección
    :param request:
    :return:
    """
    encuestas = Encuesta.objects.filter(fecha_fin__gte=datetime.now())
    eventos = Evento.objects.all()
    if request.method == 'GET':
        return render(request, 'encuestas/encuestas_creadas.html', {'encuestas': encuestas, 'eventos': eventos})
    if request.method == 'POST':
        nombre_encuesta = request.POST.get('nombre_encuesta')
        id_evento = request.POST.get('evento_id')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        survey_monkey_api = SurveyMonkeyAPI(api_key=settings.SURVEY_MONKEY_API_KEY,
                                            api_url=settings.SURVEY_MONKEY_API_URL)
        new_survey = survey_monkey_api.create_survey(title=nombre_encuesta)
        if new_survey:
            id_survey = new_survey['id']
            url_preview = new_survey['preview']
            url_edit = new_survey['edit_url']
            url_results = new_survey['analyze_url']
            Encuesta.objects.create(nombre=nombre_encuesta, evento=Evento.objects.get(id=id_evento),
                                    id_survey=id_survey, url_preview=url_preview, url_edit=url_edit,
                                    url_results=url_results, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        return render(request, 'encuestas/encuestas_creadas.html', {'encuestas': encuestas})


@rols_required(['personal_direccion', 'servicios_adicionales'])
def encuestas_creadas_historial(request):
    """
    Vista para mostrar las encuestas creadas por el personal de dirección
    :param request:
    :return:
    """
    encuestas = Encuesta.objects.filter(fecha_fin__lte=datetime.now())
    return render(request, 'encuestas/encuestas_creadas_historial.html', {'encuestas': encuestas})
