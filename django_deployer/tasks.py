import os
import yaml

from fabric.api import prompt

from django_deployer.helpers import (
    DEPLOY_YAML,
    _create_deploy_yaml,
    _validate_django_settings,
    _validate_project_name,
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

    _green("\nWe need to ask a few questions before we can deploy your Django app")

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

    requirements = prompt("* Where is your requirements.txt file?", default="requirements.txt")
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
        provider = prompt("* Which provider would you like to deploy to? \
                          (dotcloud, openshift, appengine)", validate=r".+")

    # Where to place the provider specific questions
    additional_site = {}
    if provider == "appengine":
        applicationid = prompt("* What's your Google App Engine application ID? (see https://appengine.google.com/)")
        instancename = prompt("* What's the full instance ID of your Cloud SQL instance? \
                              (should be in format \"projectid:instanceid\" \
                              found at https://code.google.com/apis/console/) ", validate=r'.+:.+')
        databasename = prompt("* What's your database name?")
        sdk_location = prompt("* Where is your Google App Engine SDK location?", default="/usr/local/google_appengine")
        additional_site.update({
            # quotes for the yaml issue
            'application_id': applicationid,
            'instancename': instancename,
            'databasename': databasename,
            'sdk_location': sdk_location
        })

    elif:
        database = prompt("* What database does your app use?", default="PostgreSQL")

    site = {
        'project_name': project_name,
        'pyversion': pyversion,
        'database': database,
        'django_settings': django_settings,
        'requirements': requirements,
        'static_url': static_url,
        'media_url': media_url,
        'provider': provider,
    }
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
