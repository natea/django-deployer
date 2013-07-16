# -*- coding: utf-8 -*-
import os

from jinja2 import Environment, PackageLoader

from django_deployer.helpers import _write_file
from django_deployer import utils

from fabric.operations import local
from fabric.context_managers import shell_env


template_env = Environment(loader=PackageLoader('django_deployer', 'paas_templates'))

def run_hooks(script_name):
    HOOKS_FOLDER = 'deployer_hooks'
    local('bash %s/%s' % (HOOKS_FOLDER, script_name) )


class PaaSProvider(object):
    """
    Base PaasProvider class. PaaS providers should inherit from this
    class and override all methods.
    """

    # Subclasses should override these
    name = ""
    setup_instructions = ""
    PYVERSIONS = {}
    provider_yml_name = "%s.yml" % name
    git_template = False
    git_template_url = ""

    @classmethod
    def init(cls, site):
        """
        put site settings in the header of the script
        """
        bash_header = ""
        for k,v in site.items():
            bash_header += "%s=%s" % (k.upper(), v)
            bash_header += '\n'
        site['bash_header'] = bash_header

        # TODO: execute before_deploy
        # P.S. running init_before seems like impossible, because the file hasn't been rendered.
        if cls.git_template:
            # do render from git repo
            print "Cloning template files..."
            repo_local_copy = utils.clone_git_repo(cls.git_template_url)
            print "Rendering files from templates..."
            target_path = os.getcwd()
            utils.render_from_repo(repo_local_copy, target_path, site)
        else:
            cls._create_configs(site)
        print cls.setup_instructions
        # TODO: execute after_deploy
        run_hooks('init_after')

    @classmethod
    def deploy(cls):
        run_hooks('deploy_before')
        run_hooks('deploy')
        run_hooks('deploy_after')

    @classmethod
    def delete(cls):
        raise NotImplementedError()

    @classmethod
    def _create_configs(cls, site):
        """
        This is going to generate the following configuration:
        * wsgi.py
        * <provider>.yml
        * settings_<provider>.py
        """
        provider = cls.name

        cls._render_config('wsgi.py', 'wsgi.py', site)

        # create yaml file
        yaml_template_name = os.path.join(provider, cls.provider_yml_name)
        cls._render_config(cls.provider_yml_name, yaml_template_name, site)

        # create requirements file
        # don't do anything if the requirements file is called requirements.txt and in the root of the project
        requirements_filename = "requirements.txt"
        if site['requirements'] != requirements_filename:   # providers expect the file to be called requirements.txt
            requirements_template_name = os.path.join(provider, requirements_filename)
            cls._render_config(requirements_filename, requirements_template_name, site)

        # create settings file
        settings_template_name = os.path.join(provider, 'settings_%s.py' % provider)
        settings_path = site['django_settings'].replace('.', '/') + '_%s.py' % provider
        cls._render_config(settings_path, settings_template_name, site)

    @classmethod
    def _render_config(cls, dest, template_name, template_args):
        """
        Renders and writes a template_name to a dest given some template_args.

        This is for platform-specific configurations
        """
        template_args = template_args.copy()

        # Substitute values here
        pyversion = template_args['pyversion']
        template_args['pyversion'] = cls.PYVERSIONS[pyversion]

        template = template_env.get_template(template_name)
        contents = template.render(**template_args)
        _write_file(dest, contents)


class Stackato(PaaSProvider):
    """
    ActiveState Stackato PaaSProvider.
    """
    name = "stackato"

    PYVERSIONS = {
        "Python2.7": "python27",
        "Python3.2": "python32",
    }

    setup_instructions = """
Just a few more steps before you're ready to deploy your app!

1. Go to http://www.activestate.com/stackato/download_client to download
   the Stackato client, and then add the executable somewhere in your PATH.
   If you're not sure where to place it, you can simply drop it in your
   project's root directory (the same directory as the fabfile.py created
   by django-deployer).

2. Once you've done that, target the stackato api with:

       $ stackato target api.stacka.to

   and then login. You can find your sandbox password at
   https://account.activestate.com, which you'll need when
   using the command:

       $ stackato login --email <email>

3. You can push your app the first time with:

       $ stackato push -n

   and make subsequent updates with:

       $ stackato update

"""

    provider_yml_name = "stackato.yml"

    def init():
        pass

    def deploy():
        pass

    def delete():
        pass


class DotCloud(PaaSProvider):
    """
    Dotcloud PaaSProvider.
    """

    name = "dotcloud"

    PYVERSIONS = {
        "Python2.6": "v2.6",
        "Python2.7": "v2.7",
        "Python3.2": "v3.2",
    }

    setup_instructions = """
        Just a few more steps before you're ready to deploy your app!

        1. Install the dotcloud command line tool with:

                $ pip install dotcloud

        2. Once you've done that, setup your Dotcloud environment for the first time:

                $ dotcloud setup
                dotCloud username or email: appsembler
                Password:
                ==> dotCloud authentication is complete! You are recommended to run `dotcloud check` now.

                $ dotcloud check
                ==> Checking the authentication status
                ==> Client is authenticated as appsembler

        3. You can create the app with:

               $ dotcloud create myapp

           and deploy it with:

               $ dotcloud push

        """

    provider_yml_name = "dotcloud.yml"

    @classmethod
    def init(cls, site):
        super(DotCloud, cls).init(site)

        # config_list: files to put in project folder, django_config_list: files to put in django project folder
        config_list = [
            'createdb.py',
            'mkadmin.py',
            'nginx.conf',
            'postinstall',
            'wsgi.py',
        ]

        # for rendering configs under root
        get_config = lambda filename: cls._render_config(filename, os.path.join(cls.name, filename), site)
        map(get_config, config_list)

    def deploy():
        pass

    def delete():
        pass


class AppEngine(PaaSProvider):
    """
    AppEngine PaaSProvider
    """

    name = 'appengine'

    PYVERSIONS = {
        "Python2.7": "v2.7"
    }

    setup_instructions = """
Just a few more steps before you're ready to deploy your app!

1. Run this command to create the virtualenv with all the packages and deploy:

        $ fab deploy

2. Create and sync the db on the Cloud SQL:

        $ sh manage.sh cloudcreatedb
        $ sh manage.sh cloudsyncdb

3. Everything is set up now, you can run other commands that will execute on your remotely deployed app, such as:

        $ sh manage.sh dbshell

"""

    provider_yml_name = "app.yaml"

    # switch to the git repo
    git_template = True
    git_template_url = "git@github.com:littleq0903/django-deployer-template-appengine.git"

    @classmethod
    def init(cls, site):
        super(AppEngine, cls).init(site)


    def delete():
        pass

class OpenShift(PaaSProvider):
    """
    OpenShift PaaSProvider
    """
    name = 'openshift'

    PYVERSIONS = {
        "Python2.6": "v2.6"
        }

    setup_instructions = ""
    git_template = True
    git_template_url = "git@github.com:littleq0903/django-deployer-template-openshift-experiment.git"

    @classmethod
    def init(cls, site):
        super(OpenShift, cls).init(site)

        #set git url to rhc

        # the first time deployment need to do "git push rhc --force"



PROVIDERS = {
    'stackato': Stackato,
    'dotcloud': DotCloud,
    'openshift': OpenShift,
    'appengine': AppEngine
}
