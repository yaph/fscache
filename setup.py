#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from setuptools import setup, find_packages
from fscache import __version__


install_requirements = Path('requirements.txt').read_text().splitlines()
test_requirements = Path('requirements_dev.txt').read_text().splitlines()

setup(
    author='Ramiro Gómez',
    author_email='code@ramiro.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='A Python package for caching data in the file system.',
    license='MIT license',
    long_description=Path('README.md').read_text(),
    include_package_data=True,
    install_requires=install_requirements,
    keywords='cache, caching, file system',
    name='fscache',
    packages=find_packages(include=['fscache']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/yaph/fscache',
    version=__version__,
    zip_safe=False
)