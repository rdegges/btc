from os.path import abspath, dirname, join, normpath

from setuptools import setup


setup(

    # Basic package information:
    name = 'btc',
    version = '0.2',
    scripts = ('btc', ),

    # Packaging options:
    zip_safe = False,
    include_package_data = True,

    # Package dependencies:
    install_requires = ['docopt>=0.6.1', 'requests>=1.2.0'],

    # Metadata for PyPI:
    author = 'Randall Degges',
    author_email = 'rdegges@gmail.com',
    license = 'UNLICENSE',
    url = 'https://github.com/rdegges/btc',
    keywords = 'bitcoin cli coinbase forex utility',
    description = 'Buy, sell, and transfer bitcoin instantly in your terminal!',
    long_description = open(normpath(join(dirname(abspath(__file__)),
        'README.md'))).read()

)
