# -*- coding: UTF-8 -*-

from setuptools import setup

import os
#~ import numpy as np
#~ import json

from setuptools import setup, Extension
from setuptools import find_packages # Always prefer setuptools over distutils
from Cython.Distutils import build_ext

def get_current_version():
    return '0.1'


#install_requires = ["numpy>0.1", "cdo>1.2", "netCDF4", "pytz", "matplotlib", 'shapely', 'cartopy', 'cython', 'scipy']



def get_packages():
    return find_packages()

setup(name='easyreport',
    version=get_current_version(),
    description='easyreport - a template based engine to allow for flexible report generation',
    packages=get_packages(),

    #package_dir={'pygvap': 'pygvap'},
    #~ package_data={'pycmbs': ['benchmarking/configuration/*',
                           #~ 'benchmarking/logo/*', 'version.json']},

    author="Alexander Loew",
    author_email='alexander.loew@lmu',
    maintainer='Alexander Loew',
    maintainer_email='alexander.loew@lmu',

    license='(c) Alexander Loew, ALL RIGHTS RESERVED, 2015-',
    # List run-time dependencies here. These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    #install_requires=install_requires,

    keywords=["report", "template"],


    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
    # How mature is this project? Common values are
    # 3 - Alpha
    # 4 - Beta
    # 5 - Production/Stable
    'Development Status :: 3 - alpha',
    # Indicate who your project is intended for
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Visualization',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2.7'
    ]


)


