import dj_database_url
import json
with open('/home/dotcloud/environment.json') as f:
  env = json.load(f)

from .settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# DB is the name of the database service defined in dotcloud.yml
# additional databases can be defined and named here (i.e. DOTCLOUD_ANOTHERDB_SQL_URL)
DATABASES = {
    "default": dj_database_url.parse(env["DOTCLOUD_DB_SQL_URL"]),
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