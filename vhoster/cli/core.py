"""Core CLI Commands"""
from .. import *
from click_alias import ClickAliasedGroup
from terminaltables import AsciiTable
import click, platform, os

def app(key=''):
    return dot_get({
        'name': 'VHoster',
        'description': 'Apache Virtual Host Manager',
        'author': 'Gerard Balaoro',
        'url': 'https://github.com/GerardBalaoro/VHoster',
        'version': '0.2.0'
    }, key, copy=True)


class State(object):
    """State Context"""

    def __init__(self, config: Config, path=None):
        self.path = os.path.abspath(path)
        self.config = config
        self.site = Site(self.config, path=self.path)
        self.server = Server(self.config)
        self.ngrok = Ngrok(self.config)

pass_state = click.make_pass_decorator(State)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(cls=ClickAliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.version_option(app('version'), '--version', '-v', message='%(version)s')
@click.pass_context
def main(ctx):
    """Apache Virtual Host Manager

    \b
    https://github.com/GerardBalaoro/VHoster  
    Copyright (c) Gerard Balaoro
    """
    if not os_supported():
        error(platform.system(), title='Platform not supported')
        raise click.Abort()

    try:
        config = Config(app_data('config.json'))
    except InvalidConfigError as err:
        raise click.ClickException(err)
        echo('Please run `config setup` to create fresh configuration')
        raise click.Abort()

    ctx.obj = State(config, path=os.getcwd())