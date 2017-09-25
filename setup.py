# Setup script for the lspcreport package
#
# Usage: python setup.py install
#
import os
from setuptools import setup, find_packages


DESCRIPTION = "lspcreport: LSPC File reader"
lspcreport = DESCRIPTION
NAME = "lspcreport"
VERSION = "0.0.1"
AUTHOR = "Lucas Nguyen (Geosyntec Consultants)"
AUTHOR_EMAIL = "lnguyen@geosyntec.com"
URL = "https://github.com/lucashtnguyen/lspcreport"
DOWNLOAD_URL = "https://github.com/lucashtnguyen/lspcreport/archive/master.zip"
LICENSE = "BSD 3-clause"
PACKAGES = find_packages()
PLATFORMS = "Python 2.7, 3.4 and later."
CLASSIFIERS = [
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Intended Audience :: Science/Research",
    "Topic :: Software Development :: Libraries :: Python Modules",
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
]
INSTALL_REQUIRES = ['pandas', 'pytest']
PACKAGE_DATA = {
    'lspcreport.tests._data': [ '*.csv', '*.out'],
}

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description=DESCRIPTION,
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    platforms=PLATFORMS,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,
    py_modules=['lspcreport']
)