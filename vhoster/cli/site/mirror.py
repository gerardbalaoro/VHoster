"""Site Mirror Commands"""
from ..core import *

@main.group()
def mirror():
    """Manage site mirrors"""
    pass


@mirror.command(short_help='Add site mirror')
@click.argument('mirror', type=str, required=True)
@click.argument('domain', type=str, required=False, default=None)
@click.option('--path', '-p', metavar='PATH', type=click.Path(exists=True, file_okay=False), default=None, help='Specify custom path')
@pass_state
def add(state, mirror, domain, path):
    """Add mirror to current (or specified) PATH or DOMAIN"""
    site = state.site
    if domain or path:
        site = site.find(domain=domain, path=path)

    if site.exists():
        site.addMirror(mirror)
        site.save()
        state.server.restart()
        success('\nSite %s mirrored to %s' % (site.domain, mirror))
    else:
        raise click.ClickException(SiteNotFoundError(domain or site.domain, path or site.path))
        raise click.Abort()


@mirror.command(short_help='Remove site mirror')
@click.argument('mirror', type=str, required=True)
@click.argument('domain', type=str, required=False, default=None)
@click.option('--path', '-p', metavar='PATH', type=click.Path(exists=True, file_okay=False), default=None, help='Specify custom path')
@pass_state
def remove(state, mirror, domain, path):
    """Remove mirror to current (or specified) PATH or DOMAIN"""
    site = state.site
    if domain or path:
        site = site.find(domain=domain, path=path)

    if site.exists():
        site.removeMirror(mirror)
        site.save()
        state.server.restart()
        success('\Mirror %s removed from %s' % (mirror, site.domain))
    else:
        raise click.ClickException(SiteNotFoundError(domain or site.domain, path or site.path))
        raise click.Abort()