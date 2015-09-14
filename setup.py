#!/usr/bin/env python
import sys
from setuptools import find_packages, setup

setup(
    name='invoices',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    author='Matt Johnson',
)
