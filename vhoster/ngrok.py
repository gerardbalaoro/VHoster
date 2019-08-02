from .helpers import *
from pyngrok import ngrok, exception


class Ngrok:
    """Ngrok Driver

    Arguments:
        config {Config} -- configuration instance
    """

    def __init__(self, config):
        self.config = config

    @property
    def configPath(self):
        """Return path to ngrok configuration file

        Returns:
            str
        """
        import os

        config = self.config.get('ngrok.config', app_data('ngrok.yml'))
        if not os.path.exists(config):
            with open(config, 'w+') as f:
                f.write('')
        return config

    @property
    def process(self):
        """Return ngrok process

        Returns:
            Popen
        """
        return ngrok.get_ngrok_process().process

    def add(self, domain, port=80):
        """Start new http tunnel

        Arguments:
            domain {str} -- domain

        Keyword Arguments:
            port {int} -- port (default: {80})

        Returns:
            str
        """
        self.stop()
        try:
            url = ngrok.connect(config_path=self.configPath, name=domain, port=80, options={
                                'host_header': domain})
            success(url, title='Now serving to public url')
            echo('Press CTRL + C to stop')
            self.process.wait()
            return url
        except exception.PyngrokError as err:
            warn(err, title='Ngrok Error')
            return

    def find(self, name):
        """Find ngrok tunnel by name

        Arguments:
            name {str} -- tunnel name

        Returns:
            NgrokTunnel
        """
        try:
            tunnels = ngrok.get_tunnels()
            for tunnel in tunnels:
                if tunnel.name == domain:
                    return tunnel
        except exception.PyngrokError as err:
            warn(err, title='Ngrok Error')
            return

    def stop(self):
        """Stop ngrok process"""
        try:
            ngrok.kill()
            success('Ngrok service stopped')
        except exception.PyngrokError as err:
            warn(err, title='Ngrok Error')
            return
