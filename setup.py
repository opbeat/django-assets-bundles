#!/usr/bin/env python
#  -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'django',
]

test_requirements = [
    'Jinja2',
]

setup(
    name='django_asset_bundles',
    version='0.0.1',
    description="Assets for Django",
    long_description=readme,
    author="Opbeat Inc.",
    author_email='vanja@opbeat.com',
    url='https://github.com/vanjacosic/django_asset_bundles',
    packages=[
        'django_asset_bundles',
    ],
    package_dir={'django_asset_bundles':
                 'django_asset_bundles'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='django_asset_bundles',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    tests_require=test_requirements,
    test_suite='runtests',
)
