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
    # TODO: identify the project dir based on where we find the settings.py or urls.py
    project_name = None
    while not project_name:
        project_name = prompt("What is your Django project's name?")
    django_settings = prompt("What is your Django settings module?", default="%s.settings" % project_name)
    requirements = prompt("Where is your requirements.txt file?", default="requirements.txt")
    _green("Tell us where your static files and uploaded media files are located")
    # TODO: eventually get these values by reading the settings.py?
    static_url = prompt("What is your STATIC_URL?", default="/static")
    static_root = prompt("Where is your STATIC_ROOT?", default="%s/static/" % project_name)
    media_url = prompt("What is your MEDIA_URL?", default="/media")
    media_root = prompt("Where is your MEDIA_ROOT?", default="%s/media/" % project_name)

    return {'pyversion': pyversion,
            'database': database,
            'project_name': project_name,
            'django_settings': django_settings,
            'requirements': requirements,
            'static_url': static_url,
            'static_root': static_root,
            'media_url': media_url,
            'media_root': media_root,
            }

def _create_deploy_yaml(site):
    _green("Creating a deploy.yml with your app's deploy info...")
    site_yaml_dict = site
    file = _join(os.getcwd(), 'deploy.yml')
    if file:
        _red("Detected an existing deploy.yml file.")
        overwrite = prompt("Overwrite your existing deploy.yml file?", default="No")
        if overwrite == "No":
            exit()

    _write_file(file, yaml.safe_dump(site_yaml_dict, default_flow_style=False))
    _green("Created %s" % file)

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

def deploy():
    site = init()
    _create_deploy_yaml(site)