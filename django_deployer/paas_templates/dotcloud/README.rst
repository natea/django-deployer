Sample apps
===========

See an example of a Django project ready to deploy to Dotcloud:
https://github.com/dotcloud/django-on-dotcloud

Tutorial
========

Tutorial for deploying a Django app to Dotcloud:
http://docs.dotcloud.com/0.4/tutorials/python/django/

Handing static assetts
======================

http://docs.dotcloud.com/0.4/tutorials/python/django/#handle-static-and-media-assets

Project layout
==============

The dotCloud directory structure will look like ::

    .
    ├── **dotcloud.yml**
    ├── hellodjango/
    │   ├── __init__.py
    │   ├── manage.py
    │   ├── settings.py
    |   |── **settings_dotcloud.py**
    │   ├── helloapp/
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   └── views.py
    │   ├── someotherapp/
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   └── views.py
    │   └── urls.py
    ├── static/
    ├── mkadmin.py
    ├── nginx.conf
    ├── **postinstall**
    ├── requirements.txt
    └── **wsgi.py**
