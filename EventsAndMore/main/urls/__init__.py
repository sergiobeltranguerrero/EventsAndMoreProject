from .main import urlpatterns_main
from .stand import urlpatterns_stand
from .evento import urlpatterns_event
from .servicios import urlpatterns_servicios
from .encuestas import urlpatterns_encuestas

urlpatterns = urlpatterns_main + urlpatterns_stand + urlpatterns_event + urlpatterns_servicios + urlpatterns_encuestas
