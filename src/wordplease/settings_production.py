import os
from .settings import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

ADMINS = (
    (os.environ.get('ADMIN_EMAIL_NAME', ''),
     os.environ.get('ADMIN_EMAIL_ADDRESS', '')),
)

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': os.environ.get('DB_NAME', ''),
       'USER': os.environ.get('DB_USER', '')
   }
}

STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get('STATIC_ROOT', "static/"))
STATIC_URL = os.environ.get('STATIC_URL', STATIC_URL)

MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get('MEDIA_ROOT', "media/"))
MEDIA_URL = os.environ.get('MEDIA_URL', "/media/")

# Para usar con HTTPS
# Forzamos la redirección HTTP a HTTPS, aunque esto ya lo hacemos con nginx (o deberíamos)
SECURE_SSL_REDIRECT = True
# Encriptamos la cookie de sesión (sólo se envía por HTTPS)
SESSION_COOKIE_SECURE = True
# Encriptamos la cookie del CSRF (sólo se envía por HTTPS)
CSRF_COOKIE_SECURE = True
