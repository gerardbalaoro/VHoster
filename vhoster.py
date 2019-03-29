import os, json, ui, re, subprocess

class VHoster(object):

    def __init__(self):
        ui.title()
        self.load()
        self.HOSTS_FILE = os.environ['SystemRoot'] + '\system32\drivers\etc\hosts'
        self.CONF_FILE = self.CONFIG['XAMPP_DIR'] + 'apache\conf\extra\httpd-vhosts.conf'

    def setup(self):
        ui.block('Create Configuration')
        self.CONFIG = {
            'XAMPP_DIR': input('Absolute Path to XAMPP Install Directory: ') or 'C:\\Xampp\\',
            'DOCUMENT_ROOR': input('Absolute Path to Document Root Folder: ') or 'C:\\Xampp\\htdocs\\'
        }

        with open('config.json', 'w+') as f:
            json.dump(self.CONFIG, f)

    def load(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                self.CONFIG = json.loads(f.read())
        else:        
            self.setup()

        ui.block('Loaded Configuration')
        for k, v in self.CONFIG.items():
            ui.line(k + ': ' + v)

    def create(self, hostname:str, path:str, port=80):
        with open(self.HOSTS_FILE, 'r+') as f:
            content = f.read()
            f.write('\n127.0.0.1 ' + hostname + ' #VHost')
            f.truncate()

        with open(self.CONF_FILE, 'r+') as f:
            content = f.read()
            f.write(
                ('\n\n## StartHost: ' + hostname + '\n<VirtualHost ' + hostname + ':' + str(port) + '>\n' +
                    '\tDocumentRoot "' + self.CONFIG['DOCUMENT_ROOT'] + path + '"\n' +
                    '\tServerName ' + hostname + '\n' +
                    '\t<Directory "' + self.CONFIG['DOCUMENT_ROOT'] + path + '">\n' +
                        '\t\tRequire all granted\n' +
                    '\t</Directory>\n' +
                '</VirtualHost>\n## EndHost')
            )
            f.truncate()

        ui.line('Virtual Host ' + hostname + ' Created')    

    def delete(self, hostname:str):
        with open(self.HOSTS_FILE, 'r+') as f:
            content = f.read()
            f.seek(0)
            f.write(re.sub('127\.0\.0\.1 ' + re.escape(hostname) + ' #VHost', '', content))
            f.truncate()

        with open(self.CONF_FILE, 'r+') as f:
            content = f.read()
            f.seek(0)
            f.write(re.sub('## StartHost: ' + re.escape(hostname) + '([\S\s]*?)## EndHost', '', content))
            f.truncate()

        ui.line('Virtual Host ' + hostname + ' Deleted')    
        

    def restart_apache(self):
        ui.line('Restarting Apache Service')
        subprocess.call([self.CONFIG['XAMPP_DIR'] + 'apache\\bin\\httpd', '-k', 'restart'])

