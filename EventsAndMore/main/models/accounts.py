from django.db.models import Model
from django.db import models
from django.contrib.auth.models import AbstractUser
from main.validator import PhoneValidator, NIFValidator


class User(AbstractUser):
    is_cliente = models.BooleanField(default=False)
    is_gestor_solicitudes = models.BooleanField(default=False)
    is_servicios_adicionales = models.BooleanField(default=False)
    is_organizador_eventos = models.BooleanField(default=False)
    is_personal_direccion = models.BooleanField(default=False)

    def __str__(self):
        return self.username + ' (' + str(self.id) + ')'

    def has_perm(self, perm, obj=None):
        if perm == 'cliente':
            return self.is_cliente
        elif perm == 'gestor_solicitudes':
            return self.is_gestor_solicitudes
        elif perm == 'servicios_adicionales':
            return self.is_servicios_adicionales
        elif perm == 'organizador_eventos':
            return self.is_organizador_eventos
        elif perm == 'personal_direccion':
            return self.is_personal_direccion
        else:
            return False


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


class Gestor_solicitudes(Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    telefono = models.CharField(max_length=14, validators=[PhoneValidator])
    NIF = models.CharField(unique=True, max_length=9, validators=[NIFValidator])
    ciutat = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.NIF


class Servicios_adicionales(Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    telefono = models.CharField(max_length=14, validators=[PhoneValidator])
    NIF = models.CharField(unique=True, max_length=9, validators=[NIFValidator])
    ciutat = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.NIF
