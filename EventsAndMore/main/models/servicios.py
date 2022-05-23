from django.db.models import Model
from django.db import models

from main.models import Cliente, Evento, Stand, Organizador_Eventos


class Servicio(Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    imagen = models.ImageField(upload_to='servicios', null=True, blank=True)
    is_generic = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre + ' (' + str(self.id) + ')'


class Servicios_Especiales(Model):
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING)


class Assignacion(Model):
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    stand = models.ForeignKey(Stand, on_delete=models.DO_NOTHING)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    ESTADO = [
        ('PD', 'Pendiente'),
        ('RC', 'Rechazada'),
        ('AP', 'Aprovada'),
    ]
    estado = models.CharField(max_length=2, choices=ESTADO, default=ESTADO[0])
    comentario = models.CharField(max_length=500, null=True)
    es_valido_por_gestor = models.BooleanField(default=False)
    es_valido_por_organizador_eventos = models.BooleanField(default=False)

    def __str__(self):
        return str(self.evento) + str(self.stand) + str(self.cliente) + ' (' + str(self.id) + ')'


class Estado_Orden(Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'


class Orden_Servicios(Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    stand = models.ForeignKey(Stand, on_delete=models.DO_NOTHING)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    estado = models.ForeignKey(Estado_Orden, on_delete=models.DO_NOTHING, default=1)

    # TODO: Preguntar que passa si un cliente que tiene mas de un stand pide el servicio se ha de poner mas de 1 si
    #  no se quita cantidad


class Servicios_Orden(Model):
    orden = models.ForeignKey(Orden_Servicios, on_delete=models.DO_NOTHING)
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()

    def subtotal(self):
        return self.servicio.precio * self.cantidad

    def __str__(self):
        return str(self.orden) + str(self.servicio) + ' (' + str(self.id) + ')'


class Carro(Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    stand = models.ForeignKey(Stand, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.cliente) + str(self.evento) + str(self.stand) + ' (' + str(self.id) + ')'


class Elementos_Carro(Model):
    carro = models.ForeignKey(Carro, on_delete=models.DO_NOTHING)
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()

    def subtotal(self):
        return self.servicio.precio * self.cantidad


class Solicitud_Servicios_Evento(Model):
    localizador = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    organizador = models.ForeignKey(Organizador_Eventos, on_delete=models.DO_NOTHING)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    solicitado = models.BooleanField(default=False)


class Servicio_Necesario(Model):
    solicitud = models.ForeignKey(Solicitud_Servicios_Evento, on_delete=DO_NOTHING)
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING)
    is_added = models.BooleanField(default=False)
