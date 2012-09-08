import yaml

from fabric.api import prompt

from django_deployer.helpers import (
    DEPLOY_YAML,
    _create_deploy_yaml,
    _read_file,
    _green,
    _yellow,
    _red,
)

from django_deployer.providers import PROVIDERS



def init(provider=None):
    _green("We need to ask a few questions before we can deploy your Django app")
    pyversion = prompt("What version of Python does your app need?", default="Python2.7")
    database = prompt("What database does your app use?", default="PostgreSQL")
    # TODO: identify the project dir based on where we find the settings.py or urls.py
    project_name = None
    while not project_name:
        project_name = prompt("What is your Django project's name?")
    django_settings = prompt("What is your Django settings module?", default="%s.settings" % project_name)
    requirements = prompt("Where is your requirements.txt file?", default="requirements.txt")

    # TODO: confirm that the file exists
    # parse the requirements file and warn the user about best practices:
    #   Django==1.4.1
    #   psycopg2 if they selected PostgreSQL
    #   MySQL-python if they selected MySQL
    #   South for database migrations
    #   dj-database-url
    _green("Tell us where your static files and uploaded media files are located")

    # TODO: get these values by reading the settings.py file
    static_url = prompt("What is your STATIC_URL?", default="/static/")
    media_url = prompt("What is your MEDIA_URL?", default="/media/")

    if not provider:
        provider = prompt("Which provider would you like to deploy to?")


    site = {
        'pyversion': pyversion,
        'database': database,
        'project_name': project_name,
        'django_settings': django_settings,
        'requirements': requirements,
        'static_url': static_url,
        'media_url': media_url,
        'provider': provider,
    }

    _create_deploy_yaml(site)

    return site

def deploy(provider=None):
    site = init(provider)

    site = yaml.safe_load(_read_file(DEPLOY_YAML))
    provider_class = PROVIDERS[site['provider']]
    provider_class._create_configs(site)
