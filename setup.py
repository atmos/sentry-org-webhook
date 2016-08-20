#!/usr/bin/env python
"""
sentry_org_webhook
==================
An extension for `Sentry <https://getsentry.com>`_ which posts all notification events for an organization to an HTTP endpoint.

:copyright: (c) 2016 Corey Donohoe
:license: MIT, see LICENSE.md for more details.
"""
from setuptools import setup, find_packages


install_requires = [
    'sentry>=8.0.0',
]

tests_require = [
    'exam',
    'flake8>=2.0,<2.1',
    'responses',
]

setup(
    name='sentry_org_webhook',
    version='0.1.0',
    author='Corey Donohoe',
    author_email='atmos@atmos.org',
    url='https://github.com/atmos/sentry-org-webhook',
    description='A Sentry extension which posts notifications to an HTTP endpoint.',
    long_description=open('README.rst').read(),
    license='BSD',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'tests': tests_require,
    },
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'org_webhook = sentry_org_webhook',
        ],
        'sentry.plugins': [
            'org_webhook = sentry_org_webhook.plugin:OrgWebhooksPlugin',
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
