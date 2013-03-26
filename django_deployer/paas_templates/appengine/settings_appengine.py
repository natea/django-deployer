try:
    import dev_appserver
    dev_appserver.fix_sys_path()
except:
    pass

from settings import *

import os
import sys

on_appengine = os.getenv('SERVER_SOFTWARE','').startswith('Google App Engine')

# insert libraries
REQUIRE_LIB_PATH = os.path.join(os.path.dirname(__file__), '..', 'env/lib/python2.7/site-packages')

lib_to_insert = [REQUIRE_LIB_PATH]
map(lambda path: sys.path.insert(0, path), lib_to_insert)

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
EMAIL_BACKEND = 'rocket_engine.email.EmailBackend'

# use Blob datastore for default file storage
DEFAULT_FILE_STORAGE = 'rocket_engine.storage.BlobStorage'

