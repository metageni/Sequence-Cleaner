#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

requirements = [
    'pysam >= 0.15.3',
    'setuptools-scm >= 3.2.0'
]

test_requirements = [
    'pytest'
]

setup_requirements = []

setup(
    name='sequence_cleaner',
    use_scm_version=True,
    description='Sequence_Cleaner: Remove Duplicate Sequences, etc',
    author='Genivaldo G.Z. Silva',
    author_email='genivaldo.gueiros@gmail.com',
    url='https://github.com/metageni/Sequence-Cleaner',
    packages=[
        'sequence_cleaner_app',
    ],
    package_dir={'sequence_cleaner_app': 'sequence_cleaner_app'},
    include_package_data=True,
    install_requires=requirements,
    setup_requires=setup_requirements,
    zip_safe=False,
    keywords='sequence_cleaner_app',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'sequence_cleaner = sequence_cleaner_app.sequence_cleaner:main',
        ]
    },
)
