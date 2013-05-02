try:
    import dev_appserver
    dev_appserver.fix_sys_path()
except:
    pass


import os
import sys

PROJECT_ROOT = os.path.dirname(__file__)

on_appengine = os.getenv('SERVER_SOFTWARE','').startswith('Google App Engine')

# insert libraries
REQUIRE_LIB_PATH = os.path.join(os.path.dirname(__file__), '..', 'site-packages')

lib_to_insert = [REQUIRE_LIB_PATH]
map(lambda path: sys.path.insert(0, path), lib_to_insert)

# settings need to be after insertion of libraries' location
from settings import *

# use cloudsql while on the production
if (on_appengine or
    os.getenv('SETTINGS_MODE') == 'prod'):
    # here must use 'SETTINGS_MODE' == 'prod', it's not included in rocket_engine.on_appengine
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'google.appengine.ext.django.backends.rdbms',
            'INSTANCE': '{{ instancename }}',
            'NAME': '{{ databasename }}',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'django_deployer_default',
            'USER': '',
            'PASSWORD': '',
        }
    }

# Installed apps for django-deployer
PAAS_INSTALLED_APPS = (
    'rocket_engine',
)

INSTALLED_APPS = tuple(list(INSTALLED_APPS) + list(PAAS_INSTALLED_APPS))

# django email backend for appengine
EMAIL_BACKEND = 'rocket_engine.mail.EmailBackend'
DEFAULT_FROM_EMAIL='example@example.com'
#NOTICE: DEFAULT_FROM_EMAIL need to be authorized beforehand in AppEngine console, you must be verified with the permission to access that mail address.
#Steps:
#1. Change DEFAULT_FROM_EMAIL above to an valid email address and you have the permission to access it.
#2. Log in to your Google App Engine Account.
#3. Under Administration, click Permissions, and add the email address.
#4. Log out, and check for the validation email.

# use Blob datastore for default file storage
DEFAULT_FILE_STORAGE = 'django-google-storage.storage.GoogleStorage'
GS_ACCESS_KEY_ID = '<fill-your-own>'
GS_SECRET_ACCESS_KEY = '<fill-your-own>'
GS_STORAGE_BUCKET_NAME = '<fill-your-own>'

if not (GS_ACCESS_KEY_ID and GS_SECRET_ACCESS_KEY and GS_STORAGE_BUCKET_NAME):
    print 'Warning: no correct settings for Google Storage, please provide it in settings_appengine.py'

# static_url
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# media url
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# use overwriting urls
ROOT_URLCONF = "{{ project_name }}.urls_appengine"
