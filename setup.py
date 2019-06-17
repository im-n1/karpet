#!/usr/bin/env python3

import setuptools
from karpet import __version__, __description__


# Long description
with open("README.rst", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="karpet",
    # version="0.1.1",
    version=__version__,
    description=__description__,
    long_description=long_description,
    author="n1",
    author_email="hrdina.pavel@gmail.com",
    url="https://github.com/im-n1/karpet",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ]
)
