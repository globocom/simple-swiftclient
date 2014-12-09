# coding: utf-8
# pylint: disable=C0103

from setuptools import setup, find_packages


setup(
    name='simple-swiftclient',
    description='A simple Openstack Swift Client to manage objects using just python standard libraries',
    url='https://github.com/globocom/simple-swiftclient',
    version='0.0.1',
    author='Time STORM',
    author_email='storm@corp.globo.com',
    packages=find_packages(),
    scripts=['bin/simpleswift'],
)
