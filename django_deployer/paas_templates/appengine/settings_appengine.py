from .settings import *

if (os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine') or
    os.getenv('SETTINGS_MODE') == 'prod'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'google.appengine.ext.django.backends.rdbms',
            'INSTANCE': '{{ instancename }}',
            'NAME': '{{ databasename }}',
        }
    }


EMAIL_BACKEND = 'rocket_engine.email.EmailBackend'

PAAS_INSTALLED_APPS = (
    'rocket_engine'
)

DEFAULT_FILE_STORAGE = 'rocket_engine.storage.BlobStorage'

if INSTALLED_APPS:
    INSTALLED_APPS += PAAS_INSTALLED_APPS
else:
    INSTALLED_APPS = PAAS_INSTALLED_APPS
