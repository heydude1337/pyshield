#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 12:56:47 2017

@author: HeyDude
"""

from setuptools import setup

README = 'README.md'
VERSION = 0.132
DESCRIPTION = ('Pyshield is a package for nuclear medicine departments to'
               'calculate the necessary amount of shielding for'
               'radionuclide labs, pet and spect scanners.')

NAME = 'pyshield'

PACKAGES = ['pyshield', 
            'pyshield.calculations', 
            'pyshield.physics', 
            'pyshield.tools']

REQUIRES = ['pandas', 
            'natsort', 
            'numpy',
            'scipy', 
            'pyyaml', 
            'xlsxwriter', 
            'matplotlib', 
            'openpyxl',
            'pathos',
            'shutil',
            'argparse']

def readme():
    with open(README) as f:
        return f.read()

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Intended Audience :: Science/Research',
        'Natural Language :: English'
      ],
      keywords='shielding nuclear medicine, isotopes, pet, spect',
      # url='https://github.com/heydude1337/pyshield',
      author='HeyDude',
      author_email='heydude1337@gmail.com',
      license='MIT',
      packages=PACKAGES,
      install_requires=REQUIRES,
      include_package_data=True,
      zip_safe=False,
      entry_points={'console_scripts':['pyshield=pyshield.__main__:main']})