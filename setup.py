# -*- coding: utf-8 -*-
# This file is part of Python Boleto.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

import setuptools

NAME = 'python-boleto'
VERSION = '0.1.0'
DESCRIPTION = 'A Python library for generating Boletos'
AUTHOR = 'Rockho Team'
AUTHOR_EMAIL = 'rockho@rockho.com.br'
URL = 'http://www.rockho.com.br/'
LICENSE = 'AGPL-3.0'

REQUIRES = [
    'Jinja2',
    'babel',
    'six',
    'iso8601'
]

TESTS_REQUIRES = [
    'pytest>=2.8.4',
    'pytest-cov>=2.2.0',
    'flake8>=2.4,<3',
    'pep8-naming>=0.2,<1',
    'iso8601'
]

EXTRAS_REQUIRES = {
    'all': set(REQUIRES + TESTS_REQUIRES)
}

if __name__ == '__main__':
    setuptools.setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        url=URL,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        packages=["python_boleto"],
        install_requires=REQUIRES,
        extras_require=EXTRAS_REQUIRES,
        tests_require=TESTS_REQUIRES,
        include_package_data=True,
    )
