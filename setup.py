import os
from setuptools import setup, find_packages

VERSION = '0.1'
NAME = 'evolene'

DIST_NAME = '{}-{}.tar.gz'.format(NAME, VERSION)
os.environ['DIST_NAME'] = DIST_NAME

setup(name='evolene',
      version=VERSION,
      description='KTH CD/CI pipeline tool',
      url='https://gita.sys.kth.se/Infosys/evolene',
      author='Jens Tinglev',
      author_email='tinglev@kth.se',
      license='MIT',
      zip_safe=False,
      packages=find_packages())
