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
@pass_state
def setup(state):
    """Create fresh configuration"""
    import json

    if os.path.exists(state.config.path):
        click.confirm(click.style('Existing configuration was found. Overwrite?', fg='yellow'), abort=True)

    def crawl(data:dict, skip=[], parents=[]):
        for key, attrs in data.get('properties', {}).items():
            fullkey = '.'.join(parents + [key])
            if fullkey not in skip and (False if [x for x in parents if x in skip] else True):
                if attrs.get('type') == 'object':
                    crawl(attrs, skip=skip, parents=parents + [key])
                else:
                    types = {'string': str, 'boolean': bool, 'integer': int}
                    is_path = [x for x in attrs.get('is_path', '').split('|') if x]
                    defaults = {
                        'dns.file': hosts_path(), 
                        'apache.sites': app_data('conf'), 
                        'apache.certs': app_data('certs'),
                        'ngrok.config': app_data('ngrok.yml')
                    }
                    prompt = {
                        'text': attrs.get('description') or attrs.get('title'),
                        'type': click.Path(
                            exists='exists' in is_path,
                            file_okay='file' in is_path,
                            dir_okay='dir' in is_path
                        ) if is_path else types.get(attrs.get('type'), str),
                        'default': defaults.get(fullkey, attrs.get('default', None)),
                        'prompt_suffix': '\n >> '
                    }
                    
                    if prompt['type'] == bool:
                        value = click.confirm(prompt['text'], default=prompt['default'])
                    else:
                        value = click.prompt(**prompt)
                    state.config.set(fullkey, value, create=True)

    schema = json.loads(template('config.schema'))
    crawl(schema, skip='sites')
    state.config.save()
    click.secho('\nConfiguration file saved', fg='green')



@config.command()
@pass_state
def path(state):
    """Get path to configuration file"""
    echo(state.config.path)