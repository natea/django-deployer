# -*- coding: utf-8 -*-
import os

from jinja2 import Environment, PackageLoader

from django_deployer.helpers import _write_file


template_env = Environment(loader=PackageLoader('django_deployer', 'paas_templates'))



class PaaSProvider(object):
    """
    Base PaasProvider class. PaaS providers should inherit from this
    class and override all methods.
    """

    def init():
        raise NotImplementedError()

    def deploy():
        raise NotImplementedError()

    def delete():
        raise NotImplementedError()

    @classmethod
    def _create_configs(cls, site):
        provider = cls.name

        cls._render_config('wsgi.py', 'wsgi.py', site)

        yaml_template_name = os.path.join(provider, '%s.yml' % provider)
        cls._render_config('%s.yml' % provider, yaml_template_name, site)

        settings_template_name = os.path.join(provider, 'settings_%s.py' % provider)
        settings_path = site['django_settings'].replace('.', '/') + '_%s.py' % provider
        cls._render_config(settings_path, settings_template_name, site)

    @classmethod
    def _render_config(cls, dest, template_name, template_args):
        """
        Renders and writes a template_name to a dest given some template_args.
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
        "Python2.7" : "python27",
        "Python3.2" : "python32",
    }

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
        "Python2.6" : "v2.6",
        "Python2.7" : "v2.7",
        "Python3.2" : "v3.2",
    }

    def init(self, site):
        super(DotCloud, self).init(site)
        
        cls._render_config('createdb.py', os.path.join(self.name, 'createdb.py'), site)
        cls._render_config('mkadmin.py', os.path.join(self.name, 'mkadmin.py'), site)
        cls._render_config('nginx.conf', os.path.join(self.name, 'nginx.conf'), site)
        cls._render_config('postinstall', os.path.join(self.name, 'postinstall'), site)

    def deploy():
        pass

    def delete():
        pass

PROVIDERS = {
    'stackato' : Stackato,
    'dotcloud' : DotCloud,
}
