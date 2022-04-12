from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from stdnum.es import dni, iban, nif
import phonenumbers


def DNIValidator(value):
    if not dni.is_valid(value):
        raise ValidationError(
            _('%(value) is not an even a DNI'),
            params={'value': value},
        )
    else:
        return value


def NIFValidator(value):
    if not nif.is_valid(value):
        raise ValidationError(
            _('%(value)s no es un NIF correcto'),
            params={'value': value},
        )
    else:
        return value


def IBANValidator(value):
    if not iban.is_valid(value):
        raise ValidationError(
            _('%(value)s is not an even a IBAN'),
            params={'value': value},
        )
    else:
        return value


def PhoneValidator(value):
    if phonenumbers.is_valid_number(phonenumbers.parse(value, "ES")):
        return value
    else:
        raise ValidationError(
            _('%(value)s no es un número de teléfono correcto'),
            params={'value': value},
        )


def NIFUniqueValidator(value):
    from .models import Cliente
    if Cliente.objects.filter(NIF=value).exists():
        raise ValidationError(
            _('%(value)s ya está en uso'),
            params={'value': value},
        )
    else:
        return value


def UniqueEmailValidator(value):
    from .models import User
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            _('%(value)s ya está en uso'),
            params={'value': value},
        )
    else:
        return value
