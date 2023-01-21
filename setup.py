# setup.py
from setuptools import setup, find_packages

setup(
    name='search',
    version='2.4.0',
    author='Travis Avery',
    python_requires='>=3.7',
    packages=find_packages(),
    install_requires=[
        'ply',
        'six',
    ],
)