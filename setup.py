#!/usr/bin/env python

from setuptools import setup

setup(name='kelly_criterion',
      version='1.0',
      author='Tibor Kiss',
      author_email='tibor.kiss@gmail.com',
      description='Kelly Criterion Calculator',
      license='Apache License, Version 2.0',
      url='http://github.com/tibkiss/kelly-criterion',
      py_modules=['kelly_criterion'],
      classifiers=['Development Status :: 6 - Mature',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 2.7',
                   'Operating System :: OS Independent',
                   'Environment :: Console',
                   'Topic :: Office/Business :: Financial :: Investment',
      ],
      keywords='option arguments parsing optparse argparse getopt',
      install_requires=['numpy>=1.9.2', 'pandas>=0.16.1', 'docopt>=0.6.2'],
	  entry_points={'console_scripts': ['kelly_criterion = kelly_criterion:main']})
