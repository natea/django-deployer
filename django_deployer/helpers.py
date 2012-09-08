import os
import re
import yaml

from fabric.api import prompt
from fabric.colors import green, red, yellow


DEPLOY_YAML = os.path.join(os.getcwd(), 'deploy.yml')



#
# Helpers
#

def _create_deploy_yaml(site):
    _green("Creating a deploy.yml with your app's deploy info...")
    site_yaml_dict = site
    file = DEPLOY_YAML
    if os.path.exists(file):
        _red("Detected an existing deploy.yml file.")
        overwrite = prompt("Overwrite your existing deploy.yml file?", default="No")
        if overwrite.strip().lower() == "no":
            exit()

    _write_file(file, yaml.safe_dump(site_yaml_dict, default_flow_style=False))
    _green("Created %s" % file)

def _validate_project_name(project_name):
    project_name_regex = r"^.+$"

    pattern = re.compile(project_name_regex)
    if not pattern.match(project_name):
        raise ValueError(red("You must enter a project name to continue!"))

    if not os.path.exists(os.path.join(os.getcwd(), project_name)):
        raise ValueError(red(
            "Couldn't find that directory name under the current directory.\n" \
            "Make sure you're using django deployer from your project root."
        ))

    return project_name


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
    """Convenience wrapper around os.path.join to make the rest of our
    functions more readable."""
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
