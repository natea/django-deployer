#!/usr/bin/env python

import os
import shutil



PACKAGE_ROOT = os.path.dirname(__file__)


def add_fabfile():
    """
    Copy the base fabfile.py to the current working directory.
    """
    fabfile_src  = os.path.join(PACKAGE_ROOT, 'fabfile.py')
    fabfile_dest = os.path.join(os.getcwd(), 'fabfile_deployer.py')

    if os.path.exists(fabfile_dest):
        print "`fabfile.py` exists in the current directory. " \
              "Please remove or rename it and try again."
        return

    shutil.copyfile(fabfile_src, fabfile_dest)
