"""Configuration CLI Commands"""
from .core import *


@main.group()
def config():
    """Manage configuration variables"""
    pass


@config.command()
@click.argument('key', metavar='KEY', type=str)
@pass_state
def get(state, key):
    """Get configuration value by KEY"""
    if key not in ['sites']:
        data = state.config.get(key)
        if type(data) in [dict, list]:
            table = []
            if isinstance(data, dict):
                table.append(['Config', 'Value'])
                for k, v in data.items():
                    table.append([str(k), str(v)])
            elif isinstance(data, list):
                for v in data:
                    table.append(data)
            echo(AsciiTable(table).table)
        else:
            echo(data)


@config.command()
@click.argument('key', metavar='KEY', type=str)
@click.argument('value', metavar='value')
@pass_state
def set(state, key, value):
    """Set configuration KEY to VALUE"""
    if key not in ['sites']:
        data = state.config.set(key, value, True)
        state.config.save()

    
@config.command()
def setup():
    """Create fresh configuration"""
    config = {
        "dns": {
            "file": click.prompt('Path to Hosts File', type=click.Path(exists=True, dir_okay=False), default=hosts_path())
        },
        "apache": {
            "bin": click.prompt('Apache Daemon Binary (httpd)', type=click.Path(exists=True, dir_okay=False)),
            "conf": click.prompt('Apache Configuration File', type=click.Path(exists=True, dir_okay=False))
        },
        "paths": {
            "conf": click.prompt('Where to store site configuration files?', type=click.Path(file_okay=False), default=app_data('conf')),
            "certs": click.prompt('Where to store site TLS certificates?', type=click.Path(file_okay=False), default=app_data('certs'))
        },
        "ngrok": {
            "config": click.prompt('Where to store ngrok configuration file?', type=click.Path(dir_okay=False), default=app_data('ngrok.yml')),
            "token": click.prompt('Ngrok authentication token', type=str, default=None)
        },
        "sites": []
    }
    with open(app_data('config.json'), 'w+') as f:
        json.dump(config, f, indent=4)
    click.secho('Configuration file saved', fg='green')


@config.command()
@pass_state
def path(state):
    """Get path to configuration file"""
    echo(state.config.path)