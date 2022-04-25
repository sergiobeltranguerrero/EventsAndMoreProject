from django.test import TestCase

from main.forms import RegisterClientForm
from main.models import Sector, User, Cliente


class RegistrationTestCase(TestCase):
    def test_registration_view(self):
        response = self.client.post('/register/client')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registerClient.html')


class RegistrationClientFormTest(TestCase):
    def test_registration_client_form(self):
        Sector.objects.create(nombre='Sector 1')
        form = RegisterClientForm({
            'username': 'testuser',
            'password1': 'EventsAndMore123',
            'password2': 'EventsAndMore123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono_contacto': '654432123',
            'nombre_empresa': 'Test Company',
            'nif': '28960520R',
            'direccion': 'Test Street',
            'poblacion': 'Test City',
            'provincia': 'Test Province',
            'pais': 'Test Country',
            'telefono_empresa': '974454084',
            'email_empresa': 'empresas@example.com',
            'sector': 1,
        })
        self.assertTrue(form.is_valid())

    def test_registration_client_form_invalid_password(self):
        Sector.objects.create(nombre='Sector 1')
        form = RegisterClientForm({
            'username': 'testuser',
            'password1': '123',
            'password2': '123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono_contacto': '654432123',
            'nombre_empresa': 'Test Company',
            'nif': '28960520R',
            'direccion': 'Test Street',
            'poblacion': 'Test City',
            'provincia': 'Test Province',
            'pais': 'Test Country',
            'telefono_empresa': '974454084',
            'email_empresa': 'empresas@example.com',
            'sector': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'][0],
                         'Esta contraseña es demasiado corta. Debe contener al menos 8 caracteres.')

    def test_registration_client_form_invalid_email(self):
        Sector.objects.create(nombre='Sector 1')
        form = RegisterClientForm({
            'username': 'testuser',
            'password1': 'EventsAndMore123',
            'password2': 'EventsAndMore123',
            'email': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono_contacto': '654432123',
            'nombre_empresa': 'Test Company',
            'nif': '28960520R',
            'direccion': 'Test Street',
            'poblacion': 'Test City',
            'provincia': 'Test Province',
            'pais': 'Test Country',
            'telefono_empresa': '974454084',
            'email_empresa': 'email',
            'sector': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], 'Introduzca una dirección de correo electrónico válida.')
        self.assertEqual(form.errors['email_empresa'][0], 'Introduzca una dirección de correo electrónico válida.')

    def test_registration_client_form_invalid_nif(self):
        Sector.objects.create(nombre='Sector 1')
        form = RegisterClientForm({
            'username': 'testuser',
            'password1': 'EventsAndMore123',
            'password2': 'EventsAndMore123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono_contacto': '654432123',
            'nombre_empresa': 'Test Company',
            'nif': '28960520A',
            'direccion': 'Test Street',
            'poblacion': 'Test City',
            'provincia': 'Test Province',
            'pais': 'Test Country',
            'telefono_empresa': '974454084',
            'email_empresa': 'empresas@example.com',
            'sector': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['nif'][0], '28960520A no es un NIF correcto')

    def test_registration_client_form_email_is_used(self):
        Sector.objects.create(nombre='Sector 1')
        User.objects.create_user(username='user', password='EventsAndMore123', email='testuser@example.com')
        form = RegisterClientForm({
            'username': 'testuser',
            'password1': 'EventsAndMore123',
            'password2': 'EventsAndMore123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono_contacto': '654432123',
            'nombre_empresa': 'Test Company',
            'nif': '28960520R',
            'direccion': 'Test Street',
            'poblacion': 'Test City',
            'provincia': 'Test Province',
            'pais': 'Test Country',
            'telefono_empresa': '974454084',
            'email_empresa': 'empresas@example.com',
            'sector': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], 'testuser@example.com ya está en uso')

    def test_registration_client_form_user_is_used(self):
        User.objects.create_user(username='user', password='EventsAndMore123')
        form = RegisterClientForm({
            'username': 'user',
            'password1': 'EventsAndMore123',
            'password2': 'EventsAndMore123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'telefono_contacto': '654432123',
            'nombre_empresa': 'Test Company',
            'nif': '28960520R',
            'direccion': 'Test Street',
            'poblacion': 'Test City',
            'provincia': 'Test Province',
            'pais': 'Test Country',
            'telefono_empresa': '974454084',
            'email_empresa': 'empresas@example.com',
            'sector': 1,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'][0], 'Ya existe un usuario con este nombre.')
