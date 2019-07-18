from setuptools import setup, find_packages

setup(
    name='VHoster',
    version='2.0',
    author='Gerard Balaoro',
    desciption='Apache Virtual Hosts Manager',
    url='https://github.com/GerardBalaoro/VHoster',
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
    entry_points='''
        [console_scripts]
        vhoster=main:cli
    ''',
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