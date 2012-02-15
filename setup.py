# -*- coding: utf-8 -*-
# Copyright (c) 2008 Ross Patterson

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import os
import sys
from setuptools import setup, find_packages

version = '0.1'

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
import instrumenting

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
HISTORY = open(os.path.join(os.path.dirname(__file__), 'HISTORY.txt')).read()

tests_require = ['zope.testing']

setup(name='instrumenting',
      version=version,
      description=instrumenting.__doc__,
      long_description=README+'\n\n'+HISTORY,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='pdb logging Python',
      author='Ross Patterson',
      author_email='me@rpatterson.net',
      url='http://github.com/rpatterson/instrumenting',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      include_package_data=True,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      test_suite = "instrumenting.tests.test_suite",
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
