from django.db.models import Model
from django.db import models
from django.contrib.auth.models import AbstractUser
from .validator import DNIValidator, PhoneValidator, IBANValidator, NIFValidator


class User(AbstractUser):
    is_cliente = models.BooleanField(default=False)
    is_gestor_solicitudes = models.BooleanField(default=False)
    is_servicios_adicionales = models.BooleanField(default=False)
    is_organizador_eventos = models.BooleanField(default=False)
    is_personal_direccion = models.BooleanField(default=False)

    def __str__(self):
        return self.username +' (' + str(self.id) + ')'

class Sector(Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Cliente(Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    telefono = models.CharField(max_length=14)
    NIF = models.CharField(unique=True, max_length=9)
    nombre_empresa = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    poblacion = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    sector = models.ForeignKey(Sector, on_delete=models.DO_NOTHING, null=True, blank=True)
    telefono_empresa = models.CharField(max_length=14)
    email_empresa = models.EmailField()
    mostrar_servicios = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_empresa


class Empleado(Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    telefono = models.CharField(max_length=14, validators=[PhoneValidator])
    DNI = models.CharField(unique=True, max_length=9, validators=[NIFValidator])
    ciutat = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.DNI

class Organizador_Evantos(Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    telefono = models.CharField(max_length=14, validators=[PhoneValidator])
    NIF = models.CharField(unique=True, max_length=9, validators=[NIFValidator])
    ciutat = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.NIF

class Servicio(Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    is_generic = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre + ' (' + str(self.id) + ')'

class Incidencia(Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre + ' (' + str(self.id) + ')'

class Comentario(Model):
    incidencia = models.ForeignKey(Incidencia, on_delete=models.DO_NOTHING)
    asunto = models.CharField(max_length=100)
    cuerpo = models.CharField(max_length=500)

    def __str__(self):
        return self.asunto + ' (' + str(self.id) + ')'

class Estado(Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre + ' (' + str(self.id) + ')'

class Evento(Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    capacidad = models.IntegerField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + ' (' + str(self.id) + ')'

class Stand(Model):
    numero_stand = models.IntegerField()

    def __str__(self):
        return self.numero_stand + ' (' + str(self.id) + ')'

class Servicios_Asignados(Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    stand = models.ForeignKey(Stand, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    # TODO: Preguntar que passa si un cliente que tiene mas de un stand pide el servicio se ha de poner mas de 1 si
    #  no se quita cantidad

    def __str__(self):
        return self.servicio + ' a '+ self.cliente +' (' + str(self.id) + ')'


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
    estado = models.CharField(max_length=2, choices=ESTADO,default=ESTADO[0])
    comentario = models.CharField(max_length=500,null=True)
    es_valido_por_gestor = models.BooleanField(default=False)
    es_valido_por_organizador_eventos = models.BooleanField(default=False)

    def __str__(self):
        return self.evento + self.stand + self.cliente +' (' + str(self.id) + ')'

class Evento_Stand_Sector(Model):
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    stand = models.ForeignKey(Stand, on_delete=models.DO_NOTHING)
    sector = models.ForeignKey(Sector, on_delete=models.DO_NOTHING)
    SIZE = [
        ( 'GR', 'Grande'),
        ('MD','Mediano'),
        ('PQ', 'Pequeño'),
    ]
    stand_size = models.CharField(max_length=2, choices=SIZE)

    def __str__(self):
        return self.evento + self.stand + self.sector +' (' + str(self.id) + ')'

    class Meta:
        unique_together = (("evento", "stand",'sector'),)


class Historial_Incidencias(Model):
    comentario = models.ForeignKey(Comentario, on_delete=models.DO_NOTHING)
    incidencia = models.ForeignKey(Incidencia, on_delete=models.DO_NOTHING)
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    def __str__(self):
        return self.incidencia + self.estado + ' (' + str(self.id) + ')'

class Carro(Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING)
    stand = models.ForeignKey(Stand, on_delete=models.DO_NOTHING)


class Elementos_Carro(Model):
    carro = models.ForeignKey(Carro, on_delete=models.DO_NOTHING)
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()

    def subtotal(self):
        return self.servicio.precio * self.cantidad
