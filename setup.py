import logging

from setuptools import find_packages
from setuptools import setup

logging.basicConfig()
VERSION = '0.0.1'
DESCRIPTION = ('Placebo is a tool for mocking '
               'external API\'s in python applications.')

setup(
    name='python-placebo',
    version=VERSION,
    description=DESCRIPTION,
    url='https://github.com/huseyinyilmaz/placebo',
    author='Huseyin Yilmaz',
    author_email='yilmazhuseyin@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    tests_require=[
        'six',
        # 'requests',
        'httmock',
        'httpretty',
    ],
)
