import ui, engine, argparse, os, json, sys
from pprint import pprint

BASE_PATH = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.realpath(__file__))

if os.path.exists(os.path.join(BASE_PATH, 'vhoster.json')):
    with open(os.path.join(BASE_PATH, 'vhoster.json'), 'r') as f:
        config = json.loads(f.read())
        vhoster = engine.VHoster(config['XAMPP_DIR'], config['DOCUMENT_ROOT'])
else:
    vhoster = engine.VHoster(BASE_PATH, os.path.join(BASE_PATH, 'htdocs'))

parser = argparse.ArgumentParser(description = 'Virtual Host Helper for XAMPP Windows')
subparsers = parser.add_subparsers(title='Availabe Commands', metavar='<command>', dest='action')
create = subparsers.add_parser('create', description='Create New Virtual Host', help='create new virtual host')
delete = subparsers.add_parser('delete', description='Delete Virtual Host', help='delete virtual host')
create.add_argument('name', type=str, help='virtual host name')
create.add_argument('path', type=str, help='host root path relative to XAMPP document root')
create.add_argument('-p', '--port', type=int, help='virtual host port number')
delete.add_argument('name', type=str, help='virtual host name')
args = parser.parse_args()


if args.action:
    if args.action == 'create':
        vhoster.delete(args.name)
        vhoster.create(args.name, args.path, args.port or 80)
    elif args.action == 'delete':
        vhoster.delete(args.name)

    vhoster.restart_apache()