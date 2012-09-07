import yaml
import os
import posixpath
import pkg_resources

from fabric.api import *
from fabric.colors import green, red, yellow
from fabric.contrib.files import exists, contains, upload_template

def init():
    _green("We need to ask a few questions before we can deploy your Django app")
    pyversion = prompt("What version of Python does your app need?", default="Python 2.7")
    database = prompt("What database does your app use?", default="PostgreSQL")
    django_settings = prompt("What is your Django settings module?", default="%s.settings" % os.path.basename(os.getcwd()))

    return {'pyversion': pyversion,
            'database': database,
            'django_settings': django_settings
            }

def _create_deploy_yaml(site, provider):
    site_yaml_dict = site
    site_yaml_dict['provider'] = provider
    file = _join(os.getcwd(), 'deploy.yml')
    _write_file(file, yaml.safe_dump(site_yaml_dict, default_flow_style=False))

def _write_file(path, contents):
    file = open(path, 'w')
    file.write(contents)
    file.close()

# pretty colors
def _green(text):
    print green(text)

def _red(text):
    print red(text)

def _yellow(text):
    print yellow(text)

def _join(*args):
    """Convenience wrapper around posixpath.join to make the rest of our
    functions more readable."""
    return posixpath.join(*args)

def deploy(provider=None):
    site = init()

    if not provider:
        provider = prompt("Which provider would you like to deploy to?", default="stackato")

    _create_deploy_yaml(site, provider)