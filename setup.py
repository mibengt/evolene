from setuptools import setup, find_packages

setup(name='evolene',
      version='0.1',
      description='KTH CD/CI pipeline tool',
      url='https://gita.sys.kth.se/Infosys/evolene',
      author='Jens Tinglev',
      author_email='tinglev@kth.se',
      license='MIT',
      zip_safe=False,
      packages=find_packages(),
      install_requires=[
          'fire == 0.1.0',
          'mock == 2.0.0',
          'coloredlogs == 6.0',
          'green == 2.7.3',
          'coverage == 4.3.4',
          'requests == 2.13.0'
      ])
