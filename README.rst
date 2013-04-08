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

From your project's root directory:

.. code:: bash

    $ deployer-init
    $ fab setup
    ...

Now inspect your project directory and you will see that a file ``deploy.yml`` and various config files were created. 

**Note:** if you're going to try different PaaS providers, it's recommended that you make a separate git branch for each one, because when you re-run ``fab setup`` it could inadvertently overwrite the config files from the first run.

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

Changelog
---------

 * 0.1.1 (26 Mar 2013) - Added support for Google App Engine (@littleq0903)
 * 0.1.0 (07 Sep 2012) - Initial version for Stackato and Dotcloud (@natea, @johnthedebs)

Roadmap
-------

 * Add support for Heroku, OpenShift and Amazon Elastic Beanstalk
 * Perform some intelligent code analysis to better guess the settings (see the djangolint project - https://github.com/yumike/djangolint)