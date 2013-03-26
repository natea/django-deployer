django-deployer
===============

Universal deployment tool for Django that currently deploys any Django app to the following PaaS providers: 
Dotcloud, Stackato and Google App Engine.

See the roadmap below for adding support for more providers: Heroku, OpenShift, Elastic Beanstalk and Gondor.

Getting Started
---------------

When it's available on PyPi you'll be available to do this:

.. code:: bash
	
    $ pip install django-deployer

Until then, you can git clone it, and from your project's virtualenv:

.. code:: bash

    $ source bin/activate
    (venv)$ git clone git://github.com/natea/django-deployer.git
    (venv)$ cd django-deployer
    (venv)$ python setup.py develop

From your project's root directory:

.. code:: bash

    $ deployer-init
    $ fab setup

To see a list of available deployer tasks use `fab --list`.

Changelog
---------

 * 0.1.1 (26 Mar 2013) - Added support for Google App Engine (@littleq0903)
 * 0.1.0 (07 Sep 2012) - Initial version for Stackato and Dotcloud (@natea, @johnthedebs)

Roadmap
-------

 * Add support for Heroku, OpenShift and Amazon Elastic Beanstalk
 * Perform some intelligent code analysis to better guess the settings (see the djangolint project - https://github.com/yumike/djangolint)