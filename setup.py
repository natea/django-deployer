#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages



setup(
    name="django-deployer",
    version="0.1.0",
    description="Django deployment utility for popular PaaS providers",
    long_description=open('README.md').read(),
    author="Nate Aune",
    author_email="nate@appsembler",
    url="https://github.com/natea/django-deployer",
    packages=find_packages(),
    install_requires=[
        'fabric==1.4.3',
        'jinja2==2.6',
        'heroku',
        'dotcloud',
        'gondor',
        'pyyaml',
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
