"""Command Line Script Modules"""
from . import *
from click_alias import ClickAliasedGroup
from terminaltables import AsciiTable
import click, os


# ------------------------------
# Application Details
# ------------------------------
def app(key=''):
    return dot_get({
        'name': 'VHoster',
        'description': 'Apache Virtual Host Manager',
        'author': 'Gerard Balaoro',
        'url': 'https://github.com/GerardBalaoro/VHoster',
        'version': 2.0
    }, key, copy=True)


# ------------------------------
# Diplay Version Info
# ------------------------------
def about(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('{name} v{version} by {author}\n{description}\n{url}'.format(**app()))
    ctx.exit()


# ------------------------------
# CLI Entry Point
# ------------------------------
@click.group(cls=ClickAliasedGroup)
@click.option('--path', metavar='PATH', default='.', type=click.Path(exists=True), help='Path to registered site')
@click.option('--version', is_flag=True, callback=about, help='Show application version', is_eager=True, expose_value=False)
@click.pass_context
def cli(ctx, path):
    """Apache Virtual Host Manager"""
    if not os_supported():
        click.secho('Platform %s not supported' % platform.system(), fg='red')
        ctx.exit()
    config_path = data_path('config.json')
    if not os.path.exists(config_path):
        click.secho('Configuration file not found', fg='yellow')
        click.echo('Running setup command...\n')
        ctx.invoke(setup)

    ctx.obj = Site(Config(config_path), path=path)


# ------------------------------
# List All Sites Command
# ------------------------------
@cli.command(aliases=['all'])
@click.pass_obj
def list(site):
    """List all registered sites"""
    table = [['Path', 'URL', 'Secure']]
    sites = site.list()
    if sites:
        for s in sites:
            table.append([
                click.style(s.path, fg='bright_yellow') + (('\n => (Root) ' + s.trueRoot()) if s.root else ''),
                click.style(s.url(), underline=True),
                click.style('Yes' if s.secure else 'No', fg='green' if s.secure else 'red')
            ])

        echo(AsciiTable(table).table)
    else:
        warn('\nNo registered sites found')


# ------------------------------
# Show Site Command
# ------------------------------
@cli.command(aliases=['info'])
@click.argument('domain', type=str, required=False, default=None)
@click.argument('path', type=click.Path(exists=True), required=False, default=None)
@click.option('--tld', metavar='TLD', type=str, default=None, help='custom TLD used by the site')
@click.pass_context
@click.pass_obj
def show(site, ctx, domain, path, tld):
    """Find site by DOMAIN or PATH and display its information"""
    if domain or path:
        site = site.find(domain=domain, path=path, tld=tld)
    
    if not site.exists():
        error('\n' + SiteNotFoundError(domain or site.domain, path or site.path).message)
        ctx.exit()
    
    table = AsciiTable([
        ['Path:', click.style(site.path, fg='bright_yellow')],
        ['URL:', click.style(site.url(), underline=True)],
        ['Secure:', click.style('Yes' if site.secure else 'No', fg='green' if site.secure else 'red')]
    ])
    table.inner_heading_row_border = False        
    echo(table.table)


# ------------------------------
# Register Site Command
# ------------------------------
@cli.command(aliases=['create'])
@click.argument('domain', type=str)
@click.argument('path', type=click.Path(exists=True), required=False, default=None)
@click.option('--root', metavar='ROOT', type=click.Path(exists=True), help='Specify custom document root for this site')
@click.option('--secure', is_flag=True, help='Enable HTTPS for this site and create self-signed certificates')
@click.option('--tld', metavar='TLD', type=str, default=None, help='Specify custom TLD for this site')
@click.option('--auto-tld', is_flag=True, help='Remove custom TLD and use default')
@click.pass_context
@click.pass_obj
def park(site, ctx, domain, path, root, secure, tld, auto_tld):
    """Register the current (or specified) PATH to given DOMAIN"""
    try:
        site.domain = domain
        if path:
            site.path = path
        if root:
            site.root = root
        if auto_tld:
            site.tld = None
        elif tld != None:
            site.tld = tld
        if secure:
            site.secure

        site.save()
        ctx.invoke(restart)
        success('\nSite registered successfully!')
        ctx.invoke(show)
    except SiteError as err:
        error('\n' + err.message)


# ------------------------------
# Forget Site Command
# ------------------------------
@cli.command(aliases=['remove'])
@click.argument('domain', type=str, required=False, default=None)
@click.argument('path', type=click.Path(exists=True), required=False, default=None)
@click.option('--tld', metavar='TLD', type=str, default=None, help='Specify custom TLD for this site')
@click.pass_context
@click.pass_obj
def forget(site, ctx, domain, path, tld):
    """Unregister the current (or specified) PATH or DOMAIN"""
    if domain or path:
        site = site.find(domain=domain, path=path, tld=tld)

    if site.exists():
        site.delete()
        ctx.invoke(restart)
        success('\nSite removed successfully!')
    else:
        error('\n' + SiteNotFoundError(domain or site.domain, path or site.path).message)


# ------------------------------
# Secure Site Command
# ------------------------------
@cli.command()
@click.argument('domain', type=str, required=False, default=None)
@click.argument('path', type=click.Path(exists=True), required=False, default=None)
@click.option('--tld', metavar='TLD', type=str, default=None, help='Specify custom TLD for this site')
@click.pass_context
@click.pass_obj
def secure(site, ctx, domain, path, tld):
    """Secure the current (or specified) PATH or DOMAIN with a trusted TLS certificate"""
    if domain or path:
        site = site.find(domain=domain, path=path, tld=tld)

    if site.exists():
        site.secure = True
        site.save()
        ctx.invoke(restart)
        success('\nSite is now available over HTTPS!')
    else:
        error('\n' + SiteNotFoundError(domain or site.domain, path or site.path).message)


# ------------------------------
# Unsecure Site Command
# ------------------------------
@cli.command()
@click.argument('domain', type=str, required=False, default=None)
@click.argument('path', type=click.Path(exists=True), required=False, default=None)
@click.option('--tld', metavar='TLD', type=str, default=None, help='Specify custom TLD for this site')
@click.pass_context
@click.pass_obj
def unsecure(site, ctx, domain, path, tld):
    """Remove trusted TLS certificate from the current (or specified) PATH or DOMAIN"""
    if domain or path:
        site = site.find(domain=domain, path=path, tld=tld)

    if site.exists():
        site.secure = False
        site.save()
        ctx.invoke(restart)
        success('\nSite TLS certificate removed!')
    else:
        error('\n' + SiteNotFoundError(domain or site.domain, path or site.path).message)



# ------------------------------
# Link Path Command
# ------------------------------
@cli.command()
@click.argument('domain', type=str, required=False, default=None)
@click.option('--tld', metavar='TLD', type=str, default=None, help='Specify custom TLD for this site')
@click.option('--auto-tld', is_flag=True, help='Remove custom TLD and use default')
@click.pass_context
@click.pass_obj
def link(site, ctx, domain, tld, auto_tld):
    """Link the current working directory to given DOMAIN"""
    if site.exists():
        site.domain = domain
        if auto_tld:
            site.tld = None
        elif tld != None:
            site.tld = tld

        site.save()
        ctx.invoke(restart)
        success('\nCurrent directory successfully linked to %s' % site.url())
    else:
        error('\n' + SiteNotFoundError(site.domain, site.path).message)


# ------------------------------
# Set Document Root Command
# ------------------------------
@cli.command(name='set-root')
@click.argument('path', type=click.Path(exists=True))
@click.argument('domain', type=str, required=False, default=None)
@click.option('--tld', metavar='TLD', type=str, default=None, help='Specify custom TLD for this site')
@click.pass_context
@click.pass_obj
def setRoot(site, ctx, path, domain, tld):
    """Set specified PATH as document root for current site or given DOMAIN"""
    if domain:
        site = site.find(domain=domain, tld=tld)

    if site.exists():
        site.root = path
        site.save()
        ctx.invoke(restart)
        success('\nSite %s document root set to  %s' % (site.url(), site.trueRoot()))
    else:
        error('\n' + SiteNotFoundError(domain or site.domain).message)


# ------------------------------
# Setup Configuration Command
# ------------------------------
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
        "paths": {
            "conf": click.prompt('Where to store site configuration files?', type=str, default='',),
            "certs": click.prompt('Where to store site TLS certificates?', type=str, default='')
        },
        "sites": []
    }
    with open(data_path('config.json'), 'w+') as f:
        json.dump(config, f, indent=4)
    click.secho('Configuration file saved', fg='green')


# ------------------------------
# Restart Apache Command
# ------------------------------
@cli.command(name='restart')
@click.pass_obj
def restart(site):
    """Restart Apache server"""
    site.server.restart()