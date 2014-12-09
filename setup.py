# -*- coding: utf-8 -*-
import codecs
import re
from os import path
from distutils.core import setup
from setuptools import find_packages


def read(*parts):
    return codecs.open(path.join(path.dirname(__file__), *parts),
                       encoding='utf-8').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-backend',
    version=find_version('django_backend', '__init__.py'),
    author=u'David Danier',
    author_email='david.danier@team23.de',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/team23/django-backend',
    license='BSD licence, see LICENSE file',
    description='A replacement of django.contrib.admin',
    long_description=u'\n\n'.join((
        read('README.rst'),
        read('CHANGES.rst'))),
    install_requires=[
        'django-floppyforms',
        'django-superform',
        # These don't have pypi releases yet.
        #'django-localstate',
        #'django-viewset',

        # Optional dependencies:
        #
        # * django-callable-perms
        # * django-assets
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
    zip_safe=False,
)
