# -*- coding: utf-8 -*-

"""
Copyright (C) 2013 Dariusz Suchojad <dsuch at zato.io>

Licensed under the BSD 3-clause license, see LICENSE.txt for terms and conditions.
"""

#
# * Django-like Redis pagination - a drop-in replacement except for the __init__ method.
#
# * Originally part of Zato - ESB, SOA and cloud integrations in Python https://zato.io
#

# flake8: noqa

from setuptools import setup, find_packages

version = '1.0'

long_description = description = 'Django-like pagination for Redis'

setup(
      name = 'zato-redis-paginator',
      version = version,

      author = 'Zato Developers',
      author_email = 'info@zato.io',
      url = 'https://github.com/zatosource/zato-redis-paginator',
      license = 'BSD 3-Clause License',
      platforms = 'OS Independent',
      description = description,
      long_description = description,

      package_dir = {'':'src'},
      packages = find_packages('src'),
      namespace_packages = ['zato'],
      
      install_requires=[
          'Django >= 1.3.1',
          'redis >= 2.4.13'
          ],
      
      keywords=('redis pagination paginate django'),
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Operating System :: POSIX :: Linux',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python',
          'Topic :: Communications',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Object Brokering',
          ],

      zip_safe = False,
)
