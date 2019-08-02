"""Site CLI Commands"""
from .core import *


@main.command()
@pass_state
def list(state):
    """List all registered sites"""
    table = AsciiTable([['Path', 'URL', 'Secure']])
    sites = state.site.list()
    if sites:
        for s in sites:
            table.table_data.append([
                click.style(s.path, fg='bright_yellow') + (('\n => (Root) ' + s.documentRoot()) if s.root else ''),
                click.style(s.url(), underline=True),
                click.style('Yes' if s.secure else 'No', fg='green' if s.secure else 'red')
            ])
        table.inner_row_border = True
        echo(table.table)
    else:
        warn('No registered sites found')


@main.command()
@click.argument('domain', type=str, required=False, default=None)
@pass_state
def show(state, domain):
    """Show information of current site or site registered to DOMAIN"""
    site = state.site
    if domain or path:
        site = site.find(domain=domain)
    
    if not site.exists():
        raise click.ClickException(SiteNotFoundError(domain or site.domain, site.path))
        raise click.Abort()
    
    table = AsciiTable([
        ['Path:', click.style(site.path, fg='bright_yellow')],
        ['Document Root:', site.documentRoot()] if site.root else ['', ''],
        ['URL:', click.style(site.url(), underline=True)],
        ['Secure:', click.style('Yes' if site.secure else 'No', fg='green' if site.secure else 'red')]
    ])
    table.inner_heading_row_border = False        
    echo(table.table)


@main.command()
@click.argument('domain', type=str, required=False, default=None)
@pass_state
def open(state, domain):
    """Open current site or site registered to DOMAIN in browser"""
    site = state.site
    if domain or path:
        site = site.find(domain=domain)
    
    if not site.exists():
        raise click.ClickException(SiteNotFoundError(domain or site.domain, site.path))
        raise click.Abort()
    
    click.launch(site.url())


@main.command()
@click.argument('domain', type=str, required=False, default=None)
@pass_state
def explore(state, domain):
    """Browse current site path or site registered to DOMAIN"""
    site = state.site
    if domain:
        site = site.find(domain=domain)
    
    if not site.exists():
        raise click.ClickException(SiteNotFoundError(domain or site.domain, site.path))
        raise click.Abort()
    
    import webbrowser
    webbrowser.open(site.path)


@main.command()
@click.argument('domain', type=str)
@click.option('--path', '-p', type=click.Path(exists=True, file_okay=False), default=None, help='Specify custom path')
@click.option('--root', '-r', metavar='ROOT', type=click.Path(exists=True), help='Specify custom document root')
@click.option('--secure', '-s', is_flag=True, help='Enable HTTPS and create self-signed certificates')
@pass_state
def park(state, domain, path, root, secure):
    """Register the current (or specified) PATH to given DOMAIN"""
    site = state.site
    try:
        if path:
            site = Site(state.config, path=path)

        site.domain = domain
        if root:
            site.root = root
        if secure:
            site.secure

        site.save()
        state.server.restart()
        success('\nSite registered successfully!')
    except SiteError as err:
        raise click.ClickException(err)
        raise click.Abort()

@main.command(aliases=['remove'])
@click.argument('domain', type=str, required=False, default=None)
@click.option('--path', '-p', type=click.Path(exists=True, file_okay=False), default=None, help='Specify custom path')
@pass_state
def forget(state, domain, path):
    """Unregister the current (or specified) PATH or DOMAIN"""
    site = state.site
    if domain or path:
        site = site.find(domain=domain, path=path)
    
    if not site.exists():
        raise click.ClickException(SiteNotFoundError(domain or site.domain, path or site.path))
        raise click.Abort()

    site.delete()
    state.server.restart()
    success('\nSite removed successfully!')
    

@main.command()
@click.argument('domain', type=str, required=False, default=None)
@click.option('--path', '-p', type=click.Path(exists=True, file_okay=False), default=None, help='Specify custom path')
@pass_state
def secure(state, domain, path):
    """Secure the current (or specified) PATH or DOMAIN with a trusted TLS certificate"""
    site = state.site
    if domain or path:
        site = site.find(domain=domain, path=path)

    if site.exists():
        site.secure = True
        site.save()
        state.server.restart()
        success('\nSite is now available over HTTPS!')
    else:
        raise click.ClickException(SiteNotFoundError(domain or site.domain, path or site.path))
        raise click.Abort()


@main.command()
@click.argument('domain', type=str, required=False, default=None)
@click.option('--path', '-p', type=click.Path(exists=True, file_okay=False), default=None, help='Specify custom path')
@pass_state
def unsecure(state, domain, path):
    """Remove trusted TLS certificate from the current (or specified) PATH or DOMAIN"""
    site = state.site
    if domain or path:
        site = site.find(domain=domain, path=path)

    if site.exists():
        site.secure = False
        site.save()
        state.server.restart()
        success('\nSite TLS certificate removed!')
    else:
        raise click.ClickException(SiteNotFoundError(domain or site.domain, path or site.path))
        raise click.Abort()


@main.command()
@click.argument('domain', type=str, required=False, default=None)
@pass_state
def link(state, domain):
    """Link the current working directory to given DOMAIN"""
    site = state.site
    if site.exists():
        site.domain = domain
        site.save()
        state.server.restart()
        success('\nCurrent directory successfully linked to %s' % site.url())
    else:
        raise click.ClickException(SiteNotFoundError(domain or site.domain, path or site.path))
        raise click.Abort()


@main.command(name='set-root')
@click.argument('path', type=click.Path(exists=True))
@click.argument('domain', type=str, required=False, default=None)
@pass_state
def setRoot(state, path, domain):
    """Set specified PATH as document root for current site or given DOMAIN"""
    site = state.site
    if domain:
        site = site.find(domain=domain)

    if site.exists():
        site.root = path
        site.save()
        state.server.restart()
        success('\nSite %s document root set to  %s' % (site.url(), site.trueRoot()))
    else:
        raise click.ClickException(SiteNotFoundError(domain or site.domain, path or site.path))
        raise click.Abort()


@main.command()
@click.argument('domain', type=str, required=False, default=None)
@click.option('--path', '-p', type=click.Path(exists=True, file_okay=False), default=None, help='Specify custom path')
@pass_state
def refresh(state, domain, path):
    """Rebuild configuration files for current (or specified) PATH or DOMAIN"""
    site = state.site
    if domain or path:
        site = site.find(domain=domain, path=path)

    if site.exists():
        site.save()
        state.server.restart()
        success('\nSite %s document root set to  %s' % (site.url(), site.trueRoot()))
    else:
        raise click.ClickException(SiteNotFoundError(domain or site.domain, path or site.path))
        raise click.Abort()


@main.command()
@pass_state
def rebuild(state):
    """Rebuild all site configuration files"""
    sites = state.site.list()
    if sites:
        for s in sites: 
            warn(s.domain, title='Rebuilding')
            s.save(force=True)
            echo('')
        state.server.restart()


@main.command()
@click.argument('domain', type=str, required=False, default=None)
@click.option('--path', '-p', type=click.Path(exists=True, file_okay=False), default=None, help='Specify custom path')
@pass_state
def share(state, domain, path):
    """Generate public url for current (or specified) PATH or DOMAIN"""
    import pyngrok

    site = state.site
    if domain or path:
        site = site.find(domain=domain, path=path)

    if site.exists():
        state.ngrok.add(site.domain, 443 if site.secure else 80)
    else:
        raise click.ClickException(SiteNotFoundError(domain or site.domain, path or site.path))
        raise click.Abort()