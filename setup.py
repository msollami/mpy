#!/usr/bin/env python

from setuptools import setup

setup(
    name='mpy',
    version='0.1.1',
    description='Mathematica style python superfunctions',
    packages=['mpy'],
    install_requires=[
        'numpy>=1.8.2,<2',
        'pytest>=2.8.7',
        'scikit-learn>=0.18,<0.19',
        'scipy>=0.19,<0.20'
    ],
    dependency_links=[
        "git+git://github.com/borntyping/python-infix.git@v1.2"
    ],
    author='Mike Sollami',
    author_email='msollami@gmail.com',
    license='MIT'
)
