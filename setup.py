import pathlib

from setuptools import setup


version = pathlib.Path(__file__).parent.joinpath('pipub', 'version.txt')
with version.open() as f:
    version = f.read().strip()

setup(version=version)
