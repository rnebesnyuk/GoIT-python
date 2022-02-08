from importlib.metadata import entry_points
from setuptools import setup, find_packages

setup(
    name='clean_folder',
    version='1.0',
    entry_points={'console_scripts': ['clean-folder=clean_folder.sort_dir:start'],},
    description='clean&sort folder script',
    author='Roman Nebesnyuk',
    author_email='rnebesnyuk@yahoo.com',
    license='MIT',
    packages=find_packages(),
)