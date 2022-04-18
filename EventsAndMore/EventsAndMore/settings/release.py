from .base import *
import django_heroku

#settings for release (do not use until first release)
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('ENGINE'),
        'NAME': os.environ.get('NAME'),
        'HOST': os.environ.get('HOST'),
        'PORT': os.environ.get('PORT'),
        'USER': os.environ.get('USER'),
        'PASSWORD': os.environ.get('PASSWORD')
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS.append('sslserver')
## that requests over HTTP are redirected to HTTPS. aslo can config in webserver
SECURE_SSL_REDIRECT = True
HTTPS=1
## X-Frame-Options
X_FRAME_OPTIONS = 'DENY'


django_heroku.settings(locals())