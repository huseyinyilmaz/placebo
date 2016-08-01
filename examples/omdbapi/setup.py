import logging
# import sys

from setuptools import find_packages
from setuptools import setup

logging.basicConfig()
VERSION = '0.0.1'
DESCRIPTION = 'example project for placebo'

setup(
    name='django-numerics',
    version=VERSION,
    description=DESCRIPTION,
    url='https://github.com/huseyinyilmaz/django-numerics',
    author='Huseyin Yilmaz',
    author_email='yilmazhuseyin@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    tests_require=[
        'requests',
    ],
)
