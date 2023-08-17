"""Set up Timescale Doctor.

Some of the code used here are based on the setup script for the tool
pip (https://github.com/pypa/pip/blob/main/setup.py).

"""

import os

from setuptools import setup, find_packages

def read(rel_path: str) -> str:
    """Read a file and return its contents."""
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), encoding='ascii') as infile:
        return infile.read()

def get_version(rel_path: str) -> str:
    """Read the version from the given file.

    Format for the version looks like this::

        __version__ = "0.9"
    """
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name = "doctor",
    version = get_version("src/doctor/__init__.py"),
    author = "Mats Kindahl",
    author_email = "mats@timescale.com",
    description ="Analyze a database and provide recommendations",
    license = "Apache 2",
    keywords = "postgresql timescale",
    project_urls={
        "Documentation": "https://pip.pypa.io",
        "Source": "https://github.com/timescale/doctor",
        "Changelog": "https://pip.pypa.io/en/stable/news/",
    },
    package_dir={"": "src"},
    packages=find_packages(where='src', exclude=['tests']),
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache 2 License",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=[
          'psycopg2',
      ],
    entry_points={
        "console_scripts": [
            "timescale-doctor=doctor:main",
        ],
    },
)
