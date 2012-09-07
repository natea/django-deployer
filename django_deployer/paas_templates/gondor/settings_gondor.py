import os

import dj_database_url

from .settings import *

DATABASES = {
    "default": dj_database_url.config(env="GONDOR_DATABASE_URL"),
}

MEDIA_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "media")

