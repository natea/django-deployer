import os
import dj_database_url

from .settings import *

DATABASES = {
    "default": dj_database_url.config(env="DATABASE_URL"),
}

MEDIA_ROOT = os.environ['STACKATO_FILESYSTEM']

