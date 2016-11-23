#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name="eppicpipeline",
    version="3.0.0-0",
    description="Tools for running EPPIC",
    url="http://github.com/eppic/eppic-pipeline",
    license="GPL2",
    install_requires=[
        "luigi  == 2.3.3",
        "pybars >= 0.0.4",
    ],
    packages=find_packages(),
    package_data={'': ['*.hbs']}

    )
