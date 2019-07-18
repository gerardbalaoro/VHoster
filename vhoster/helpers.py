import platform
import socket
import appdirs
import os
import re

def check_supported_os():
    return platform.system() in ['Windows']

def is_os(*args):
    return platform.system() in args

def data_path(*args):
    path = os.path.abspath(os.path.join(appdirs.user_data_dir(), 'vhost', *args))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path
    
def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port

def str_replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)