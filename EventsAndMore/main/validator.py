from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from stdnum.es import dni, iban, nif
import phonenumbers


def DNIValidator(value):
    if not dni.is_valid(value):
        raise ValidationError(
            _('%(value)s is not an even a DNI'),
            params={'value': value},
        )
    else:
        return value


def NIFValidator(value):
    if not nif.is_valid(value):
        raise ValidationError(
            _('%(value)s is not an even a NIF'),
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
            _('%(value)s is not an even a Phone number'),
            params={'value': value},
        )
