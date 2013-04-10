django-deployer
===============

django-deployer is a deployment tool for Django that currently deploys any Django app to the following PaaS providers: 
Dotcloud, Stackato and Google App Engine.

The goal of django-deployer is to minimize the effort to deploy a Django app to any of the popular PaaS providers. It asks a series of questions about your Django project, and then generates a generic deploy.yml file that captures all of your project's requirements. django-deployer then uses this deploy.yml file to translate these requirements into specific configurations for each PaaS. 

See the roadmap below for adding support for more providers: Heroku, OpenShift, Elastic Beanstalk and Gondor.

Getting Started
---------------

To install django-deployer, use ``pip`` to fetch the package from PyPi:

.. code:: bash
	
    $ pip install django-deployer

Now from your project's root directory run the ``deployer-init`` command once, and then run ``fab setup``. 

In this example (using `paasbakeoff <http://github.com/appsembler/paasbakeoff>`_), we are going to tell django-deployer to prepare our project to deploy to Google App Engine.

.. code:: bash

    $ deployer-init
    $ fab setup

	We need to ask a few questions before we can deploy your Django app
	* What is your Django project directory name?
	  (This usually contains your settings.py and a urls.py) mywebsite
	* What is your Django settings module? [mywebsite.settings] 
	* Where is your requirements.txt file? [requirements.txt] mywebsite/requirements/project.txt
	* What version of Python does your app need? [Python2.7] 
	* What is your STATIC_URL? [/static/] 
	* What is your MEDIA_URL? [/media/] 
	* Which provider would you like to deploy to (dotcloud, openshift, appengine)? appengine
	* What's your Google App Engine application ID (see https://appengine.google.com/)? djangodeployermezz
	* What's the full instance ID of your Cloud SQL instance (should be in format "projectid:instanceid" found at https://code.google.com/apis/console/)? djangomezzanine:djangomezzdb
	* What's your database name? appenginedemo
	* Where is your Google App Engine SDK location? [/usr/local/google_appengine] 
	Creating a deploy.yml with your app's deploy info...
	Created /Users/nateaune/Dropbox/code/paasbakeoff/deploy.yml

	Just a few more steps before you're ready to deploy your app!

	1. Run this command to create the virtualenv with all the packages and deploy:

	        $ fab deploy

	2. Create and sync the db on the Cloud SQL:

	        $ sh manage.sh cloudcreatedb
	        $ sh manage.sh cloudsyncdb

	3. Everything is set up now, you can run other commands that will execute on your remotely deployed app, such as:

	        $ sh manage.sh dbshell

	Done.

Now inspect your project directory and you will see that a file ``deploy.yml`` and various config files were created. 

**Note:** if you're going to try different PaaS providers, it's recommended that you make a separate git branch for each one, because when you re-run ``fab setup`` it could inadvertently overwrite the config files from the first run.

Upgrading
---------

You will notice that when we ran ``pip install django-deployer`` it created a script ``deployer-init``. When you ran this script, it created a fabfile.py in your current directory that imports the tasks module from the ``django-deployer`` project.

.. code:: python

	from django_deployer.tasks import *

This means that you can update the django-deployer package and don't need to regenerate the fabfile.

.. code:: bash

	$ pip install -U django-deployer


Contribute
----------

If you want to develop django-deployer, you can clone it and install it into your project's virtualenv:

.. code:: bash

    $ source bin/activate
    (venv)$ git clone git://github.com/natea/django-deployer.git
    (venv)$ cd django-deployer
    (venv)$ python setup.py develop

Or you can also install an editable source version of it using pip:

.. code:: bash

    $ source bin/activate
    (venv)$ pip install -e git+git://github.com/natea/django-deployer.git#django-deployer

Which will clone the git repo into the ``src`` directory of your project's virtualenv.

Roadmap
-------

- Add support for Heroku, OpenShift, Amazon Elastic Beanstalk and Gondor
- Perform some intelligent code analysis to better guess the settings (see the djangolint project - https://github.com/yumike/djangolint)
- Write tests!
- Caching (Redis, Memcache)
- Celery
- Email
- SSL
