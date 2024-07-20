# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Raspi-utin',
    version='0.0.1',
    description='Weather forecast e-Paper Display',
    long_description=readme,
    author='Gonzalo Ortiz',
    author_email='gonzalo.ortiz.lavado@protonmail.com',
    url='https://github.com/gortizlavado/RasPi-utin.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
