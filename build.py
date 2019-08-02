import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    '--name=vhoster',
    '--onefile',
    '--hidden-import=appdirs',
    '--icon=favicon.ico',
    'vhoster/bin/vhoster',
])