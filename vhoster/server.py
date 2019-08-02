import subprocess, os
from .helpers import *
from .config import Config

class Server:
    """Apache Server Driver

    Arguments:
        config {Config} -- configuration instance
    """

    def __init__(self, config: Config):
        self.config = config

    @property
    def path(self):
        """Return path to apache binary
        
        Returns:
            str
        """
        return self.config.get('apache.bin', 'httpd')

    def run(self, *args):
        """Run apache commands
        
        Returns:
            dict -- {command, returncode, output, errors}
        """
        return run_command('"{bin}" {args}'.format(bin=self.path, args=' '.join(args)))

    def start(self):
        """Start apache service"""
        self.run('-k', 'start')
        success('Apache service started')

    def stop(self):
        """Stop apache service"""
        self.run('-k', 'stop')
        warn('Apache service stopped')

    def restart(self):
        """Restart apache service"""
        self.run('-k', 'restart')
        success('Apache service restarted')