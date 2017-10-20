# Setup script for the hymo package
#
# Usage: python setup.py install
#
import os
from setuptools import setup, find_packages


DESCRIPTION = "hymo: EPA SWMM Report File reader"
NAME = "hymo"
VERSION = "0.1.0"
AUTHOR = "Lucas Nguyen (Geosyntec Consultants)"
AUTHOR_EMAIL = "lnguyen@geosyntec.com"
URL = "https://github.com/lucashtnguyen/hymo"
DOWNLOAD_URL = "https://github.com/lucashtnguyen/hymo/archive/master.zip"
LICENSE = "BSD 3-clause"
PACKAGES = find_packages()
PLATFORMS = "Python 3.4, 3.5 and later."
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
    'hymo.tests._data.lspc': [ '*.csv', '*.rpt', '*.inp', '*.out'],
    'hymo.tests._data.swmm': [ '*.csv', '*.rpt', '*.inp', '*.out'],
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
    py_modules=['hymo']
)