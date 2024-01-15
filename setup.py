from setuptools import setup
from setuptools import find_packages

setup(
    name='delta-vacuum-ls',
    version="0.0.1",
    author='mrk',
    author_email='mrk@sed.pl',
    install_requires=[
        "deltalake",
        "more-itertools",
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'delta-vacuum-ls=delta_vacuum_ls:main',
        ]
    }
)