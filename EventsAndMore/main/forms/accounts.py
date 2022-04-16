from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.db import transaction

from main.models import Cliente, Sector
from main.validator import NIFValidator, PhoneValidator, NIFUniqueValidator, UniqueEmailValidator


class RegisterClientForm(UserCreationForm):
    telefono_contacto = forms.CharField(max_length=14, required=True, label='Teléfono del contacto',
                                        validators=[PhoneValidator])
    nombre_empresa = forms.CharField(max_length=100, required=True, label='Nombre de la empresa')
    nif = forms.CharField(max_length=9, required=True, label='NIF', validators=[NIFValidator, NIFUniqueValidator])
    direccion = forms.CharField(max_length=100, required=True, label='Dirección')
    poblacion = forms.CharField(max_length=50, required=True, label='Población')
    provincia = forms.CharField(max_length=50, required=True, label='Provincia')
    pais = forms.CharField(max_length=50, required=True, label='País')
    telefono_empresa = forms.CharField(max_length=14, required=True, label='Teléfono de la empresa',
                                       validators=[PhoneValidator])
    email_empresa = forms.EmailField(max_length=50, required=True, label='Email de la empresa',
                                     validators=[EmailValidator])
    sector = forms.ModelChoiceField(queryset=Sector.objects.all(), required=True, label='Sector')
    first_name = forms.CharField(max_length=50, required=True, label='Nombre del contacto')
    last_name = forms.CharField(max_length=50, required=True, label='Apellidos del contacto')
    email = forms.EmailField(max_length=50, required=True, label='Email del contacto',
                             validators=[EmailValidator, UniqueEmailValidator])

    class Meta(UserCreationForm.Meta):
        User = get_user_model()
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_cliente = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        cliente = Cliente.objects.create(user=user)
        cliente.telefono = self.cleaned_data['telefono_contacto']
        cliente.nombre_empresa = self.cleaned_data['nombre_empresa']
        cliente.NIF = self.cleaned_data['nif']
        cliente.direccion = self.cleaned_data['direccion']
        cliente.poblacion = self.cleaned_data['poblacion']
        cliente.provincia = self.cleaned_data['provincia']
        cliente.pais = self.cleaned_data['pais']
        cliente.telefono_empresa = self.cleaned_data['telefono_empresa']
        cliente.email_empresa = self.cleaned_data['email_empresa']
        cliente.sector = self.cleaned_data['sector']
        cliente.save()

        return user


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput)
    new_password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    new_password_confirmation = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput)

    def clean_new_password_confirmation(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirmation = self.cleaned_data.get('new_password_confirmation')

        if new_password and new_password_confirmation and new_password != new_password_confirmation:
            raise forms.ValidationError('Las contraseñas no coinciden')

        return new_password_confirmation
