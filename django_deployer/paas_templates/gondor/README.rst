Tutorial
========

This is a tutorial for how to deploy a Django app with Gondor:
https://gondor.io/support/django/setup/

Sample apps
===========

Sample Django project ready to deploy to Gondor:
https://github.com/eldarion/gondor-project-django

Project layout
==============

Here is a sample directory structure for a Django project:

gondor-project-django/
    .git or .hg (version control metadata)
    fixtures/
        initial_data.json (where any data that should be loaded into the database on each deploy)
    **gondor.yml** (Gondor configuration file)
    manage.py
    project_name/ (project's Python package)
        __init__.py
        settings.py
        **settings_gondor.py** (Django settings for use on Gondor)
        static/ (see README in directory)
        templates/ (where templates for your project goes)
        urls.py
        **wsgi.py** (WSGI entry point for Django)
    requirements.txt (pip file to declare dependencies) 