#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name="django-deployer",
    version="0.1.2",
    description="Django deployment tool for popular PaaS providers",
    long_description=open('README.rst').read() + '\n\n' +
                     open('CHANGES.txt').read(),
    keywords="PaaS Django Dotcloud Stackato Heroku Gondor AWS OpenShift GAE appengine fabric deployment",
    author="Nate Aune",
    author_email="nate@appsembler.com",
    url="http://natea.github.io/django-deployer",
    license="MIT",
    packages=find_packages(),
    package_data={
        '': ['*.txt', '*.rst'],
        'django_deployer': ['paas_templates/*/*'],
    },
    install_requires=[
        'fabric==1.6.0',  # formerly 1.4.3
        'jinja2==2.6',
        'heroku==0.1.2',
        'dotcloud==0.9.4',
        'gondor==1.2.2',
        'pyyaml==3.10',
        'sphinx==1.1.3',
        'requests==0.14.2',
    ],
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ),
    entry_points={
        'console_scripts': [
            'deployer-init = django_deployer.main:add_fabfile',
        ]
    },
)
