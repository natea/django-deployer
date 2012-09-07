Sample apps
===========

See an example of a Django project ready to deploy to Dotcloud:
https://github.com/dotcloud/django-on-dotcloud

Tutorial
========

Tutorial for deploying a Django app to Dotcloud:
http://docs.dotcloud.com/0.4/tutorials/python/django/

Project layout
==============

.
├── dotcloud.yml
├── hellodjango/
│   ├── __init__.py
│   ├── manage.py
│   ├── settings.py
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
├── postinstall*
├── requirements.txt
└── wsgi.py