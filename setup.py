#!/usr/bin/env python

from setuptools import setup

setup(name='kelly_criterion',
      version='1.0',
      author='Tibor Kiss',
      author_email='tibor.kiss@gmail.com',
      description='Kelly Criterion Calculator',
      long_description='Optimal leverage calculation for financial securities using Kelly Criterion',
      license='BSD 3 Clause License',
      url='http://github.com/tibkiss/kelly-criterion',
      py_modules=['kelly_criterion'],
      classifiers=['Development Status :: 6 - Mature',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 2.7',
                   'Operating System :: OS Independent',
                   'Environment :: Console',
                   'Topic :: Office/Business :: Financial :: Investment',
      ],
      keywords='kelly formula criterion finance optimal leverage',
      install_requires=['numpy>=1.9.2', 'pandas>=0.16.1', 'docopt>=0.6.2'],
      entry_points={'console_scripts': ['kelly_criterion = kelly_criterion:main']})
