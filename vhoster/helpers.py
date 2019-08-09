"""Helper Methods"""


def is_os(*args):
    """Check if current OS is in args
    
    Returns:
        bool
    """
    import platform
    return platform.system() in args


def os_supported():
    """Check if current OS is supported
    
    Returns:
        bool
    """
    return is_os('Windows')


def app_data(*args):
    """Return path to application data
    
    Returns:
        str
    """
    import click, os
    path = os.path.abspath(os.path.join(
        click.get_app_dir('VHoster', roaming=False), *args))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def hosts_path():
    """Return path to system hosts file

    Returns:
        str
    """
    if is_os('Windows'):
        return 'C:/Windows/System32/drivers/etc/hosts'
    else:
        return '/etc/hosts'


def valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.

    Arguments:
        s {str}

    Returns:
        str
    """
    import re
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '-', s)


def dot_get(data, key='', default=None, copy=False):
    """Retrieve key value from data using dot notation
    
    Arguments:
        data {mixed} -- data source
    
    Keyword Arguments:
        key {str} -- key using dot notation (default: {''})
        default {mixed} -- default value if key does not exist (default: {None})
        copy {bool} -- create a copy of the value (to break memory refence) (default: {False})
    
    Returns:
        mixed
    """
    from copy import deepcopy
    nodes = [n for n in [n.strip() for n in key.split('.') if n]]

    if nodes:
        for i, node in enumerate(nodes):
            if isinstance(data, dict):
                if i + 1 == len(nodes) and node in data.keys():
                    return data[node]
                else:
                    if node in data.keys():
                        data = data[node]
                    else:
                        break
    else:
        return deepcopy(data) if copy else data

    return default


def get_free_tcp_port():
    """Get unbound TCP port from localhost
    
    Returns:
        int
    """
    import socket
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


def is_port_open(port):
    """Check if port is open
    
    Arguments:
        port {int} -- port
    
    Returns:
        bool
    """
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        port = int(port)
        return not s.connect_ex(('localhost', port)) == 0


def parse_host(url, default_port:int=None):
    import re
    pattern = r"^(?P<domain>[a-zA-Z0-9.-]+)(:?)(?P<port>[0-9]*?)$"
    matches = re.search(pattern, url)
    return {'domain': matches.groupdict().get('domain'), 'port': matches.groupdict().get('port') or default_port}


def str_replace(string, substitutions: dict):
    """Replace multiple parts of string
    
    Arguments:
        string {str} -- source string
        substitutions {dict} -- dictionary of substitutions
    
    Returns:
        str
    """
    import re
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)


def run_command(command, quiet=False):
    """Run shell command using subprocess
    
    Arguments:
        command {str} -- command to execute
    
    Keyword Arguments:
        quiet {bool} -- suppress output (default: {False})
    
    Returns:
        dict -- {command, return code, output, errors}
    """
    import subprocess, shlex
    proc = subprocess.Popen(shlex.split(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    if not quiet:
        stdout, stderr = b'', b''
        for line in proc.stdout:
            stdout += line
            echo(line.decode(), nl=False)
        for line in proc.stderr:
            stderr += line
            error(line.decode(), nl=False)
        proc.communicate()
    else:
        stdout, stderr = proc.communicate()
    return {'command': command, 'returncode': proc.returncode, 'output': stdout.decode(), 'errors': stderr.decode()}


def template(name, **substitutions):
    """Load template from resources
    
    Arguments:
        name {str} -- template name
    
    Returns:
        str
    """
    from importlib_resources import read_text
    from pyratemp import Template
    from . import templates
    return Template(read_text(templates, name))(**substitutions, f={
        'parse_host': parse_host,
        'is_port_open': is_port_open
    })


def echo(message, title=None, style=None, pre='',**kwargs):
    """Print message to stdout
    
    Arguments:
        message {str}
    
    Keyword Arguments:
        title {str} -- optional text title (default: {None})
        style {str} -- text foreground color (default: {None})
        pre {str} -- line prefix
    """
    import click
    click.echo(pre + (click.style(str(title) + ': ', fg=style) if title else '') + click.style(str(message), fg=None if title else style), **kwargs)


def info(message, **kwargs):
    """Print info message to stdout
    
    Arguments:
        message {str}
    """
    echo(message, style='cyan', **kwargs)


def success(message, **kwargs):
    """Print success message to stdout
    
    Arguments:
        message {str}
    """
    echo(message, style='green', **kwargs)


def error(message, **kwargs):
    """Print error message to stdout
    
    Arguments:
        message {str}
    """
    echo(message, style='red', **kwargs)


def warn(message, **kwargs):
    """Print warning message to stdout
    
    Arguments:
        message {str}
    """
    echo(message, style='yellow', **kwargs)
