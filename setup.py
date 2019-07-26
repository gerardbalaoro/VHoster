from setuptools import setup, find_packages
from vhoster.cli import app

setup(
    name=app('name'),
    version=app('version'),
    author=app('author'),
    desciption=app('description'),
    url=app('url'),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'appdirs',
        'colorama',
        'cryptography',
        'appdirs',
        'importlib-resources',
        'terminaltables'
    ],
    entry_points = {
        'console_scripts': ['vhoster=vhoster.bin.vhoster'],
    },
    package_data={
        '': ['*.md', '*.txt', 'LICENSE', 'README', '*.ico'],
        'vhoster': ['*.json', '*.conf'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
)