from setuptools import setup

setup(
  name='tsdlv',
  version='0.1.0',
  author='Brad Schneider',
  author_email='bradschneider14@gmail.com',
  packages=['tsdlv', 'tsdlv.common', 'tsdlv.session'],
  url='https://github.com/bradschneider14/tsdlv',
  license='LICENSE.txt',
  description='A package providing a server application for viewing time series log data',
  install_requires=[
      "flask",
  ],
)