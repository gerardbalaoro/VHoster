import os, ui, re, subprocess, sys

class VHoster(object):

    def __init__(self, XAMPP_DIR, DOCUMENT_ROOT):
        ui.title()
        self.XAMPP_DIR = os.path.abspath(XAMPP_DIR)
        self.DOCUMENT_ROOT = os.path.abspath(DOCUMENT_ROOT)

        ui.block(['XAMPP Directory: ' + self.XAMPP_DIR, 'Document Root: ' + self.DOCUMENT_ROOT], 'Loaded Configuration')
        if not os.path.exists(self.XAMPP_DIR) or not os.path.exists(self.DOCUMENT_ROOT):
            ui.block('XAMPP Directory or Document Root Not Found', 'Error')
            sys.exit(1)

        self.HOSTS_FILE = os.path.join(os.environ['SystemRoot'], 'system32\\drivers\\etc\\hosts')
        self.CONF_FILE = os.path.join(self.XAMPP_DIR,'apache\\conf\\extra\\httpd-vhosts.conf')

    def create(self, hostname:str, path:str, port=80):
        ui.line('Creating ' + hostname + ':' + str(port) + ', at ' + path)
        with open(self.HOSTS_FILE, 'r+') as f:
            ui.line('Writing system hosts file')
            content = f.read()
            f.write('\n127.0.0.1 ' + hostname + ' #VHost')
            f.truncate()

        with open(self.CONF_FILE, 'r+') as f:
            ui.line('Writing apache vhosts configuration')  
            content = f.read().strip()
            f.write(
                '\n\n## StartHost: ' + hostname + '\n<VirtualHost ' + hostname + ':' + str(port) + '>\n' +
                    '\tDocumentRoot "' + os.path.abspath(os.path.join(self.DOCUMENT_ROOT, path)) + '"\n' +
                    '\tServerName ' + hostname + '\n' +
                    '\t<Directory "' + os.path.abspath(os.path.join(self.DOCUMENT_ROOT, path)) + '">\n' +
                        '\t\tRequire all granted\n' +
                    '\t</Directory>\n' +
                '</VirtualHost>\n## EndHost'
            )
            f.truncate()

    def delete(self, hostname:str):
        ui.line('Removing ' + hostname)
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
            ui.line('Writing apahe vhosts configuration')
            content = f.read().strip()
            f.seek(0)
            f.write(re.sub('## StartHost: ' + re.escape(hostname) + '([\S\s]*?)## EndHost', '', content).strip())
            f.truncate()  
        

    def restart_apache(self):
        ui.line('Restarting apache service')
        subprocess.call([os.path.join(self.XAMPP_DIR, 'apache\\bin\\httpd.exe'), '-k', 'restart'])