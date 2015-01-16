#!/usr/bin/env python
"""
# sentry-safe-github

A limited alternavite to sentry-github which doesn't require write access to
repos. It allows creating tickets but doesn't link them to the sentry error
group.
"""


from setuptools import setup, find_packages


# tests_require = [
#     'nose',
# ]

install_requires = [
    'sentry>=6.0.0',
]

setup(
    name='sentry-safe-github',
    version='0.1',
    author='Daniel Benamy',
    author_email='dbenamy@stripe.com',
    url='https://github.com/stripe/sentry-safe-github',
    description='Create github tickets from sentry errors. More secure but less featureful than sentry-github.',
    long_description=__doc__,
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    # tests_require=tests_require,
    # extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    include_package_data=True,
    entry_points={
       'sentry.apps': [
            'safe_github = sentry_safe_github',
        ],
       'sentry.plugins': [
            'safe_github = sentry_safe_github.plugin:SafeGithubPlugin',
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
