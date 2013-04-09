import json

with open('/home/dotcloud/environment.json') as f:
    env = json.load(f)

from .settings import *


if 'DOTCLOUD_DATA_MYSQL_HOST' in env:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env['DOTCLOUD_PROJECT'],
            'USER': env['DOTCLOUD_DATA_MYSQL_LOGIN'],
            'PASSWORD': env['DOTCLOUD_DATA_MYSQL_PASSWORD'],
            'HOST': env['DOTCLOUD_DATA_MYSQL_HOST'],
            'PORT': int(env['DOTCLOUD_DATA_MYSQL_PORT']),
        }
    }
elif 'DOTCLOUD_DB_SQL_HOST' in env:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env['DOTCLOUD_PROJECT'],
            'USER': env['DOTCLOUD_DB_SQL_LOGIN'],
            'PASSWORD': env['DOTCLOUD_DB_SQL_PASSWORD'],
            'HOST': env['DOTCLOUD_DB_SQL_HOST'],
            'PORT': int(env['DOTCLOUD_DB_SQL_PORT']),
        }
    }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "propagate": True,
        },
    }
}