#!/usr/bin/env python3

import setuptools
from karpet.meta import __version__, __description__


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
    install_requires=[
        "numpy >= 1.16.4",
        "pandas >= 0.24.2",
        "requests >= 2.22.0",
        "beautifulsoup4 >= 4.7.1",
        "lxml >= 4.3.4",
        "aiohttp >= 3.5.4",
    ],
    extras_require={
        "twitter": ["twitterscraper == 1.1.0"],
        "google": ["pytrends >= 4.6.0"],
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/im-n1/karpet/issues",
        "Documentation": "https://github.com/im-n1/karpet",
        "Source Code": "https://github.com/im-n1/karpet",
    },
)
