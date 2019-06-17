import os, ui, re, subprocess, sys
from config import Config

class VHoster(object):

    def __init__(self, CONFIG_PATH):
        ui.title()
        self.config = Config(CONFIG_PATH)
        if self.config.validate() == False:
            ui.line('Configuration Error')
            self.config.generate()

        self.DOCUMENT_ROOT = self.config('document_root')
        self.HOSTS_FILE = self.config('hosts_file')
        self.CONF_FILE = self.config('vhosts_conf_path')

    def configure(self):
        ui.line('Configuring Application')
        self.config.generate()
        ui.line('Configuration Saved')    

    def add(self, hostname:str, path:str, port=80):
        ui.line('Creating ' + hostname + ':' + str(port) + ', at ' + path)
        with open(self.HOSTS_FILE, 'r+') as f:
            ui.line('Writing System Hosts File')
            content = f.read()
            f.write('\n127.0.0.1 ' + hostname + ' #VHost')
            f.truncate()

        with open(self.CONF_FILE, 'r+') as f:
            ui.line('Writing Apache Configuration')  
            content = f.read().strip()
            f.write(
                '\n\n## StartHost: ' + hostname + ':' + str(port) + '\n<VirtualHost *:' + str(port) + '>\n' +
                    '\tDocumentRoot "' + os.path.abspath(os.path.join(self.DOCUMENT_ROOT, path)) + '"\n' +
                    '\tServerName ' + hostname + '\n' +
                    '\t<Directory "' + os.path.abspath(os.path.join(self.DOCUMENT_ROOT, path)) + '">\n' +
                        '\t\tRequire all granted\n' +
                    '\t</Directory>\n' +
                '</VirtualHost>\n## EndHost'
            )
            f.truncate()

        ui.line('Virtual Host Created')

    def remove(self, hostname:str, port=80, quiet=False):
        if not quiet:
            ui.line('Removing ' + hostname + ':' + str(port))
        with open(self.HOSTS_FILE, 'r+') as f:
            content = []
            for line in f:
                line = line.strip()
                if line != '' and not re.match('127\.0\.0\.1 ' + re.escape(hostname) + ' #VHost', line) and not line in content:
                    content.append(line)
            f.seek(0)
            f.write('\n'.join(content))
            f.truncate()
            

        with open(self.CONF_FILE, 'r+') as f:
            ui.line('Writing Apache Configuration')
            content = f.read().strip()
            f.seek(0)
            f.write(re.sub('## StartHost: ' + re.escape(hostname) + ':' + str(port) + '([\S\s]*?)## EndHost', '', content).strip())
            f.truncate()  
        
        if not quiet:
            ui.line('Virtual Host Removed')
        
    def list(self):
        ptrn = r"## StartHost: (\S*)\s*<VirtualHost \*:(\d*)>\s*DocumentRoot \"(\S*)\"\s*ServerName (\S*)\n\s*[\s\S]*?## EndHost"
        conf = open(self.CONF_FILE, 'r').read()
        hosts = re.findall(ptrn, conf)
        ui.line('Listing Active Virtual Hosts', '\n\n')
        for host in hosts:
            ui.line('Host Name: ' + host[0])
            ui.line('Document Root: ' + host[2], '\n\n')

    def restart_apache(self):
        ui.line('Restarting Apache Service')
        proc = subprocess.run(self.config('apache_restart').split(' '), encoding='utf-8', stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        for line in proc.stdout.split('\n'):
            if line.strip() != '':
                ui.line(line)