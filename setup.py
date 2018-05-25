# -*- coding: utf-8 -*-
import os
from setuptools import setup

packages = []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('odym'):
    # Ignore dirnames that start with '.'
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)

setup(
    name='odym',
    version="0.0.1",
    packages=packages,
    author="IndEcol",
    license=open('LICENSE').read(),
    install_requires=[
        'xlrd',
        'xlwt',
        'scipy',
        'pandas',
        'pypandoc',
    ],
    url="https://github.com/IndEcol/ODYM",
    long_description=open('README.md').read(),
    description=('Open Dynamic Material Systems Model'),
)
