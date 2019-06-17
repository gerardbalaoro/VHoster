import ui, engine, argparse, os, json, sys
from pprint import pprint
from config import Config

BASE_PATH = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.realpath(__file__))
parser = argparse.ArgumentParser(description = 'Virtual Host Helper for XAMPP Windows')
subparsers = parser.add_subparsers(title='Availabe Commands', metavar='<command>', dest='action')

subcommands = {
    'add': {
        'description': 'Add New Virtual Host',
        'params': [
            {'name': 'name', 'type': str, 'help': 'server name'},
            {'name': 'path', 'type': str, 'help': 'server root (relative to DOCUMENT_ROOT'},
            {'name': '--port','type': int, 'help': 'server port'},
        ]
    },
    'remove': {
        'description': 'Remove Virtual Host',
        'params': [
            {'name': 'name', 'type': str, 'help': 'server name'},
            {'name': '--port','type': int, 'help': 'server port'},
        ]
    },
    'hosts': {
        'description': 'List Active Virtual Hosts'
    },
    'config': {
        'description': 'Configure Application'
    }
}

for subcommand, meta in subcommands.items():
    vars()[subcommand] = subparsers.add_parser(subcommand, description=meta['description'], help=meta['description'].lower())
    if 'params' in meta.keys():
        for param in meta['params']:        
            vars()[subcommand].add_argument(param['name'], type=param['type'], help=param['help'])

args = parser.parse_args()
if args.action and args.action in list(subcommands.keys()):
    vhoster = engine.VHoster(os.path.join(BASE_PATH, 'vhoster.ini'))
    if args.action == 'config':
        vhoster.configure()
    elif args.action == 'hosts':
        vhoster.list()
    else:
        if args.action == 'add':
            vhoster.remove(args.name, args.port or 80, True)
            vhoster.add(args.name, args.path, args.port or 80)
        elif args.action == 'remove':
            vhoster.remove(args.name, args.port or 80)
        vhoster.restart_apache()
