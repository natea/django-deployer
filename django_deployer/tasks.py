import os
import yaml

from fabric.api import prompt

from django_deployer.helpers import (
    DEPLOY_YAML,
    _create_deploy_yaml,
    _validate_django_settings,
    _validate_project_name,
    _validate_managepy,
    _validate_requirements,
    _read_file,
    _green,
    _yellow,
    _red,
)

from django_deployer.providers import PROVIDERS


def init(provider=None):
    """
    Runs through a questionnaire to set up your project's deploy settings
    """
    if os.path.exists(DEPLOY_YAML):
        _yellow("\nIt looks like you've already gone through the questionnaire.")
        cont = prompt("Do you want to go through it again and overwrite the current one?", default="No")

        if cont.strip().lower() == "no":
            return None
    _green("\nWelcome to the django-deployer!")
    _green("\nWe need to ask a few questions in order to set up your project to be deployed to a PaaS provider.")

    # TODO: identify the project dir based on where we find the settings.py or urls.py
    project_name = prompt(
        "* What is your Django project directory name?\n" \
        "  (This usually contains your settings.py and a urls.py)",
        validate=_validate_project_name
    )

    django_settings = prompt(
        "* What is your Django settings module?",
        default="%s.settings" % project_name,
        validate=_validate_django_settings
    )

    managepy = prompt(
        "* Where is your manage.py file?",
        default="%s/manage.py" % project_name,
        validate=_validate_managepy
    )

    requirements = prompt(
        "* Where is your requirements.txt file?", 
        default="requirements.txt",
        validate=_validate_requirements
    )
    # TODO: confirm that the file exists
    # parse the requirements file and warn the user about best practices:
    #   Django==1.4.1
    #   psycopg2 if they selected PostgreSQL
    #   MySQL-python if they selected MySQL
    #   South for database migrations
    #   dj-database-url

    pyversion = prompt("* What version of Python does your app need?", default="Python2.7")

    # TODO: get these values by reading the settings.py file
    static_url = prompt("* What is your STATIC_URL?", default="/static/")
    media_url = prompt("* What is your MEDIA_URL?", default="/media/")

    if not provider:
        provider = prompt("* Which provider would you like to deploy to (dotcloud, openshift, appengine)?", validate=r".+")

    # Where to place the provider specific questions
    site = {}
    additional_site = {}

    if provider == "appengine":
        applicationid = prompt("* What's your Google App Engine application ID (see https://appengine.google.com/)?")
        instancename = prompt("* What's the full instance ID of your Cloud SQL instance (should be in format \"projectid:instanceid\" found at https://code.google.com/apis/console/)?", validate=r'.+:.+')
        databasename = prompt("* What's your database name?")
        sdk_location = prompt("* Where is your Google App Engine SDK location?", default="/usr/local/google_appengine")
        additional_site.update({
            # quotes for the yaml issue
            'application_id': applicationid,
            'instancename': instancename,
            'databasename': databasename,
            'sdk_location': sdk_location,
        })

        # only option with Google App Engine is MySQL, so we'll just hardcode it
        site = {
            'database': 'MySQL'
        }

    else:
        database = prompt("* What database does your app use?", default="PostgreSQL")
        site = {
            'database': database,
        }

    # TODO: add some validation that the admin password is valid
    admin_password = prompt("* What do you want to set as the admin password?")

    site.update({
        'project_name': project_name,
        'pyversion': pyversion,
        'django_settings': django_settings,
        'managepy': managepy,
        'requirements': requirements,
        'static_url': static_url,
        'media_url': media_url,
        'provider': provider,
        'admin_password': admin_password,
    })

    site.update(additional_site)

    _create_deploy_yaml(site)

    return site


def setup(provider=None):
    """
    Creates the provider config files needed to deploy your project
    """
    site = init(provider)
    if not site:
        site = yaml.safe_load(_read_file(DEPLOY_YAML))

    provider_class = PROVIDERS[site['provider']]
    provider_class.init(site)


def deploy(provider=None):
    """
    Deploys your project
    """
    if os.path.exists(DEPLOY_YAML):
        site = yaml.safe_load(_read_file(DEPLOY_YAML))

    provider_class = PROVIDERS[site['provider']]
    provider_class.deploy(site)
