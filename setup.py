# Setup script for the swmmreport package
#
# Usage: python setup.py install
#
import os
from setuptools import setup, find_packages


DESCRIPTION = "swmmreport: EPA SWMM Report File reader"
swmmreport = DESCRIPTION
NAME = "swmmreport"
VERSION = "0.0.1"
AUTHOR = "Lucas Nguyen (Geosyntec Consultants)"
AUTHOR_EMAIL = "lnguyen@geosyntec.com"
URL = "https://github.com/lucashtnguyen/swmmreport"
DOWNLOAD_URL = "https://github.com/lucashtnguyen/swmmreport/archive/master.zip"
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
INSTALL_REQUIRES = ['pandas']
PACKAGE_DATA = {
    'swmmreport.tests._data': [ '*.csv', '*.rpt'],
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
)