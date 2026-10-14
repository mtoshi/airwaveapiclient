# -*- coding: utf-8 -*-

"""airwaveapiclient setup.py"""

from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
import sys
import os


class Tox(TestCommand):

    """Tox."""

    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        """Init."""
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        """Finalize."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Run."""
        import tox
        import shlex
        if self.tox_args:
            errno = tox.cmdline(args=shlex.split(self.tox_args))
        else:
            errno = tox.cmdline(self.tox_args)
        sys.exit(errno)


classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: System :: Monitoring",
    "Topic :: System :: Networking",
]

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as _file:
    README = _file.read()

requires = []
req_file = os.path.join(here, 'requirements.txt')
if os.path.exists(req_file):
    with open(req_file) as _file:
        requires = [line.strip() for line in _file if line.strip() and not line.startswith('#')]
if not requires:
    requires = ['requests', 'xmltodict']

setup(
    name="airwaveapiclient",
    version="0.1.12",
    description='Aruba Networks AirWave API Client.',
    long_description=README,
    author='Toshikatsu Murakoshi',
    author_email='mtoshi.g@gmail.com',
    url='https://github.com/mtoshi/airwaveapiclient',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
    data_files=[],
    python_requires=">=3.6",
    install_requires=requires,
    include_package_data=True,
    tests_require=['tox'],
    cmdclass={'test': Tox},
)
