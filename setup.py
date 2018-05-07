#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
    'aiohttp',
    'sanic',
    'sanic-jwt'
]

setup_requirements = [
    # TODO(manqx): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='auth-api',
    description="Access Sanic-jwt encrypted data.",
    author="Man QuanXing",
    author_email='manquanxing@gmail.com',
    url='https://github.com/manqx/iologik',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'auth-api=client.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords=['sanic', 'sanic-jwt', 'aiohttp'],
    classifiers=['Environment :: Console'],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
