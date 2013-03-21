from .settings import *

# use cloudsql while on the production
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
elif not DATABASES:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'django_deployer_default',
            'USER': '',
            'PASSWORD': '',
        }
    }



# django email backend for appengine
EMAIL_BACKEND = 'rocket_engine.email.EmailBackend'

INSTALLED_APPS = tuple()

# Installed apps for django-deployer
PAAS_INSTALLED_APPS = (
    'rocket_engine',
)

try:
    INSTALLED_APPS = tuple(list(INSTALLED_APPS) + list(PAAS_INSTALLED_APPS))
except NameError:
    pass

# use Blob datastore for default file storage
DEFAULT_FILE_STORAGE = 'rocket_engine.storage.BlobStorage'

