#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='invoices',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    author='Matt Johnson',
    extras_require={
        'test': [
            'model_mommy',
            'mock',
            'django<1.9',
            'isort',
            'flake8',
        ],
    }
)
