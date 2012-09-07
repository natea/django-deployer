import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'{{ project_name }}')))
os.environ['DJANGO_SETTINGS_MODULE'] = '{{ django_settings }}_stackato'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()