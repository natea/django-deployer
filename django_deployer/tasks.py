import yaml

from fabric.api import prompt

from django_deployer.helpers import (
    DEPLOY_YAML,
    _create_deploy_yaml,
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
    _green("\nWe need to ask a few questions before we can deploy your Django app")

    # TODO: identify the project dir based on where we find the settings.py or urls.py
    project_name = prompt(
        "* What is your Django project directory name?\n" \
        "  (This usually contains your settings.py and a urls.py)",
        validate=_validate_project_name
    )
    django_settings = prompt("* What is your Django settings module?", default="%s.settings" % project_name)

    requirements = prompt("* Where is your requirements.txt file?", default="requirements.txt")
    # TODO: confirm that the file exists
    # parse the requirements file and warn the user about best practices:
    #   Django==1.4.1
    #   psycopg2 if they selected PostgreSQL
    #   MySQL-python if they selected MySQL
    #   South for database migrations
    #   dj-database-url

    pyversion = prompt("* What version of Python does your app need?", default="Python2.7")
    database = prompt("* What database does your app use?", default="PostgreSQL")

    # TODO: get these values by reading the settings.py file
    static_url = prompt("* What is your STATIC_URL?", default="/static/")
    media_url = prompt("* What is your MEDIA_URL?", default="/media/")

    if not provider:
        provider = prompt("* Which provider would you like to deploy to?", default="stackato")

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

    _create_deploy_yaml(site)

    return site

def deploy(provider=None):
    """
    Creates the provider config files needed to deploy your project
    """
    site = init(provider)

    site = yaml.safe_load(_read_file(DEPLOY_YAML))
    provider_class = PROVIDERS[site['provider']]
    provider_class._create_configs(site)
