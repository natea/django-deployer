import os
import re
import yaml

from fabric.colors import green, red, yellow


DEPLOY_YAML = os.path.join(os.getcwd(), 'deploy.yml')


#
# Helpers
#

def _create_deploy_yaml(site):
    _green("Creating a deploy.yml with your app's deploy info...")
    _write_file(DEPLOY_YAML, yaml.safe_dump(site, default_flow_style=False))
    _green("Created %s" % DEPLOY_YAML)


def _validate_django_settings(django_settings):
    django_settings_regex = r"^[\d\w_.]+$"

    pattern = re.compile(django_settings_regex)
    if not pattern.match(django_settings):
        raise ValueError(red("You must enter a valid dotted module path to continue!"))

    django_settings_path = django_settings.replace('.', '/') + '.py'
    if not os.path.exists(django_settings_path):
        raise ValueError(red(
            "Couldn't find a settings file at that dotted path.\n"
            "Make sure you're using django-deployer from your project root."
        ))

    return django_settings


def _validate_project_name(project_name):
    project_name_regex = r"^.+$"

    pattern = re.compile(project_name_regex)
    if not pattern.match(project_name):
        raise ValueError(red("You must enter a project name to continue!"))

    if not os.path.exists(os.path.join(os.getcwd(), project_name)):
        raise ValueError(red(
            "Couldn't find that directory name under the current directory.\n"
            "Make sure you're using django-deployer from your project root."
        ))

    return project_name


def _validate_requirements(requirements):

    if not requirements.endswith(".txt"):
        raise ValueError(red("Requirements file must end with .txt"))

    if not os.path.exists(os.path.join(os.getcwd(), requirements)):
        raise ValueError(red(
            "Couldn't find requirements.txt at the path you gave.\n"
            "Make sure you're using django-deployer from your project root."
        ))

    return requirements


def _validate_managepy(managepy):
    managepy_regex = r"^.+manage.py$"

    pattern = re.compile(managepy_regex)
    if not pattern.match(managepy):
        raise ValueError(red(
            "Couldn't find manage.py at the path you gave.\n"
            "You must enter the relative path to your manage.py file to continue!"
        ))

    if not os.path.exists(os.path.join(os.getcwd(), managepy)):
        raise ValueError(red(
            "Couldn't find manage.py at the path you gave.\n"
            "Make sure you're using django-deployer from your project root."
        ))

    return managepy


#
# Utils
#

def _write_file(path, contents):
    file = open(path, 'w')
    file.write(contents)
    file.close()


def _read_file(path):
    file = open(path, 'r')
    contents = file.read()
    file.close()
    return contents


def _join(*args):
    """
    Convenience wrapper around os.path.join to make the rest of our
    functions more readable.
    """
    return os.path.join(*args)


#
# Pretty colors
#

def _green(text):
    print green(text)


def _red(text):
    print red(text)


def _yellow(text):
    print yellow(text)
