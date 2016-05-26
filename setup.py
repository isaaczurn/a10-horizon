#!/usr/bin/env python
# flake8: noqa

from setuptools import setup, find_packages

setup(
    name = "a10-horizon",
    version = "0.1.5",
    packages = find_packages(),

    author = "A10 Networks",
    author_email = "dougw@a10networks.com",
    description = "A10 Networks Openstack Horizon Dashboard",
    license = "Apache",
    keywords = "a10 adc slb load balancer openstack neutron lbaas horizon",
    url = "https://github.com/a10networks/a10-horizon",

    long_description = open('README.md').read(),

    classifiers = [
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
    ],

    include_package_data=True,

    scripts=['scripts/a10-horizon'],

    install_requires = ['a10-neutronclient>=0.1.4']
)
