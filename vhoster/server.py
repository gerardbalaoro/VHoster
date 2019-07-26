import subprocess, os
from .helpers import *
from .config import Config

class Server:

    def __init__(self, config: Config):
        self.config = config

    @property
    def apache(self):
        return self.config.get('apache.bin', 'httpd')

    def install(self, config):
        if is_os('Windows'):
            run_command(self.apache + ' -k install')
            success('Apache is installed')

    def uninstall(self):
        if is_os('Windows'):
            run_command(self.apache + ' -k uninstall')
            success('Apache is uninstalled')

    def start(self):
        run_command(self.apache + ' -k start')
        success('Apache service started')

    def stop(self):
        run_command(self.apache + ' -k stop')
        warn('Apache service stopped')

    def restart(self):
        run_command(self.apache + ' -k restart')
        success('Apache service restarted')

    def info(self):
        run_command(self.apache + ' -v')