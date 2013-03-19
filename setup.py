#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages



setup(
    name="django-deployer",
    version="0.1.0",
    description="Django deployment utility for popular PaaS providers",
    long_description=open('README.rst').read(),
    author="Nate Aune",
    author_email="nate@appsembler.com",
    url="https://github.com/natea/django-deployer",
    packages=find_packages(),
    install_requires=[
        'fabric==1.6.0',  # formerly 1.4.3
        'jinja2==2.6',
        'heroku',
        'dotcloud',
        'gondor',
        'pyyaml',
        'sphinx==1.1.3',
        'requests==0.14.2',
    ],
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPL License",
        "Programming Language :: Python",
    ),
    entry_points={
        'console_scripts' : [
            'deployer-init = django_deployer.main:add_fabfile',
        ]
    },
)
