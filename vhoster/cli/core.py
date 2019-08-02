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
        'version': '2.0.0'
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

@click.group(cls=ClickAliasedGroup)
@click.version_option(app('version'), '--version', '-v', message='%(version)s')
@click.help_option('--help', '-h')
@click.pass_context
def main(ctx):
    """Apache Virtual Host Manager"""
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


@main.command()
def version():
    """Show application information"""
    echo('%s (v%s): %s' % (click.style(app('name'), 'cyan'), app('version'), app('description')))