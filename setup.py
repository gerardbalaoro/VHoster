from setuptools import setup, find_packages
from vhoster.cli import app

setup(
    name=app('name'),
    version=app('version'),
    author=app('author'),
    description=app('description'),
    url=app('url'),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'colorama',
        'cryptography',
        'pyratemp',
        'click-alias',
        'pyngrok',
        'importlib-resources',
        'terminaltables'
    ],
    entry_points = {
        'console_scripts': ['vhoster=vhoster.cli:main']
    },
    package_data={
        '': ['*.md', '*.txt', 'LICENSE', 'README', '*.ico'],
        'vhoster': ['*.json', '*.conf']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows"
    ]
)