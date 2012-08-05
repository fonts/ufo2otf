#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description…
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ufo2otf",
    version = "0.1.0",
    author = "Eric Schrijver",
    author_email = "eric@ericschrijver.nl",
    description = ("Take UFO font sources and generate OTF’s and webfonts"),
    license = "BSD",
    keywords = "font utility web ufo otf conversion command line",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['ufo2otf'],
    scripts=['bin/ufo2otf'],
    long_description=read('README.rst'),
    classifiers=[
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
