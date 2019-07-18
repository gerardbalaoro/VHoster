import platform
import colorama
import click
import json
import os
from vhoster.errors import *
from vhoster.helpers import *
from vhoster.site import Site
from vhoster.config import Config
from click_alias import ClickAliasedGroup
from terminaltables import AsciiTable


APP_INFO = {
    'name': 'VHoster',
    'description': 'Apache Virtual Host Manager',
    'author': 'Gerard Balaoro',
    'url': 'https://github.com/GerardBalaoro/VHoster',
    'version': 2.0
}

CONFIG = None
SITE = None

def about(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('{name} v{version} by {author}\n{description}\n{url}'.format(**APP_INFO))
    ctx.exit()
    
@click.group(cls=ClickAliasedGroup)
@click.option('--version', is_flag=True, callback=about, is_eager=True, expose_value=False)
@click.pass_context
def cli(ctx):
    """Apache Virtual Host Manager"""
    if not check_supported_os():
        click.secho('Platform %s not supported' % platform.system(), fg='red')
        os._exit(1)
    config_path = data_path('config.json')
    if not os.path.exists(config_path):
        click.secho('Configuration file not found', fg='yellow')
        click.echo('Running setup command...\n')
        ctx.invoke(setup)

    CONFIG = Config(data_path('config.json'))
    SITE = Site(CONFIG)

@cli.command(aliases=['park'])
@click.argument('domain', type=str)
@click.argument('path', type=str)
@click.option('--secure', is_flag=True)
def create(domain, path, secure):
    """Register given domain using specified path as root"""
    try:
        site = SITE.create(domain, path, secure)
        path = os.path.abspath(path)
        if site:
            click.secho('Site %s linked to %s' % (domain, path), fg='green')
    except SiteError as error:
        click.secho(error.message, fg='yellow')

@cli.command(aliases=['forget'])
@click.argument('domain', type=str)
def remove(domain):
    """Unregister given domain"""
    try:
        site = SITE.delete(domain)
        if site:
            click.secho('Site %s unregistered' % domain, fg='green')
    except SiteError as error:
        click.secho(error.message, fg='yellow')

@cli.command()
@click.argument('old', type=str)
@click.argument('new', type=str)
def rename(old, new):
    """Change site domain name"""
    try:
        site = SITE.rename(old, new)
        if site:
            click.secho('Site %s renamed to %s' % (old, new), fg='green')
    except SiteError as error:
        click.secho(error.message, fg='yellow')

@cli.command()
@click.argument('domain', type=str)
@click.argument('path', type=str)
def link(domain, path):
    """Link directory as root to existing site"""
    try:
        site = SITE.link(domain, path)
        path = os.path.abspath(path)
        if site:
            click.secho('Site %s linked to %s' % (domain, path), fg='green')
    except SiteError as error:
        click.secho(error.message, fg='yellow')

@cli.command()
def list():
    """List all registered sites"""
    sites = SITE.list()
    table = [['Domain', 'Path', 'Secured']]
    for site in sites:
        table.append([
            'http%s://%s' % ('https' if site['secure'] else '', SITE.getHostName(site['domain'])),
            os.path.abspath(site['path']), 
            'Yes' if site['secure'] else 'No'
        ])
    table = AsciiTable(table)
    click.echo(table.table)

@cli.command()
@click.argument('domain', type=str)
def find(domain):
    """Find registered site by domain"""
    site = SITE.find(domain)
    if site:
        table = AsciiTable([
            ['Domain', 'Path', 'Secured'],
            [
                'http%s://%s' % ('https' if site['secure'] else '', SITE.getHostName(site['domain'])),
                os.path.abspath(site['path']), 
                'Yes' if site['secure'] else 'No'
            ]
        ])
        click.echo(table.table)
    else:
        click.secho('Site %s not found' % domain, fg='red')


@cli.command()
@click.argument('domain', type=str)
def secure(domain):
    """Secure given domain with a trusted TLS certificate"""
    try:
        site = SITE.secure(domain)
        if site:
            click.secho('Site %s secured with TLS certificate' % domain, fg='green')
    except SiteError as error:
        click.secho(error.message, fg='yellow')

@cli.command()
@click.argument('domain', type=str)
def unsecure(domain):
    """Stop serving the given domain over HTTPS and remove the trusted TLS certificate"""
    try:
        site = SITE.secure(domain)
        if site:
            click.secho('TLS certificate removed from %s' % domain, fg='green')
    except SiteError as error:
        click.secho(error.message, fg='yellow')

@cli.command(name='refresh-all')
def refreshAll():
    """Refresh all site configuration files"""
    try:
        SITE.refreshAll()
        click.secho('All configuration files have been regenerated', fg='green')
    except SiteError as error:
        click.secho(error.message, fg='yellow')\

@cli.command()
@click.argument('domain', type=str)
def refresh(domain):
    """Refresh configuration files for specific site"""
    try:
        SITE.refreshAll()
        click.secho('Configuration files for %s have been regenerated' % domain, fg='green')
    except SiteError as error:
        click.secho(error.message, fg='yellow')

@cli.command()
def setup():
    """Configure Vhoster"""
    config = {
        "tld": click.prompt('Default TLD (Domain Extension)', type=str, default='test'),
        "dns": {
            "file": click.prompt('Path to Hosts File', type=str, default="C:/Windows/System32/drivers/etc/hosts")
        },
        "apache": {
            "bin": click.prompt('Path to Apache Daemon Binary (httpd)', type=str),
            "conf": click.prompt('Path to Apache Configuration File', type=str)
        },
        "collection": [],
        "sites": []
    }
    with open(data_path('config.json'), 'w+') as f:
        json.dump(config, f, indent=4)
    click.secho('Configuration file saved', fg='green')

@cli.command(name='apache:restart')
def apacheRestart():
    """Restart Apache server"""
    SITE.server.restart()
    click.secho('Apache daemon started', fg='green')

