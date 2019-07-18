import subprocess, os
from .helpers import *
from .config import Config
from .console import Console

class Server:

    def __init__(self, config: Config):
        self.console = Console()
        self.config = config

    def install(self, config):
        if is_os('Windows'):
            self.console.run(self.config.get('apache.bin'), '-k', 'install')

    def uninstall(self):
        if is_os('Windows'):
            self.console.run(self.config.get('apache.bin'), '-k', 'uninstall')

    def start(self):
        self.console.run(self.config.get('apache.bin'), '-k', 'start')

    def stop(self):
        self.console.run(self.config.get('apache.bin'), '-k', 'stop')

    def restart(self):
        self.console.run(self.config.get('apache.bin'), '-k', 'restart')

    def info(self):
        self.console.run(self.config.get('apache.bin'), '-v')