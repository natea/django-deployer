import dj_database_url

from .settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    "default": dj_database_url.config(env="DATABASE_URL"),
}

SITE_ID = 1 # set this to match your Sites setup

MEDIA_ROOT = os.path.join(os.environ["UWSGI_STATIC_URL"], "site_media", "media")
STATIC_ROOT = os.path.join(os.environ["UWSGI_STATIC_URL"], "site_media", "static")
