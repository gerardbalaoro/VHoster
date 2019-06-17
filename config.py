from configparser import ConfigParser
from pathlib import Path
import platform, re

class Config:

    def __init__(self, path):
        self.path = path
        self.config = ConfigParser(allow_no_value=True)
        self.config.read(self.path)    
    
    def __call__(self, name, fallback=None):
        return self.get(name, fallback)

    def schema(self):
        return {
            'paths': {
                'DOCUMENT_ROOT': 'Document Root Directory (htdocs)',
                'VHOSTS_CONF_PATH': 'Virtual Hosts Configuration File (httpd-vhosts.conf)',
                'APACHE_BIN': 'Apache Binaries Directory',
                'HOSTS_FILE': 'System Hosts File ::auto'
            },
            'commands': {
                'APACHE_RESTART': 'Restart Apache Service ::auto'
            }
        }

    def get(self, name, fallback=None):
        section, option = name.split('.') if '.' in name else ('*', name)
        if section == '*':
            for s in self.config.sections():
                if option.lower() in self.config.options(s):
                    section = s 
                    break;
            else:
                return fallback    
        value = self.config.get(section, option.lower())
        args = re.findall(r"\$([\w]*)", value)
        for arg in args:
            sub = self.get(arg)
            if sub != None:
                value = value.replace('$' + arg, sub)
        return value            

    def generate(self):
        for section, options in self.schema().items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for option, label in options.items():
                label = label.split(' ::')
                prmpt = label[0] + ' (leave blank to auto generate)' if 'auto' in label else label[0]
                value = input('   >> ' + prmpt + ' :: ')
                self.config.set(section, option, value if value != '' else self.auto(option))

        with open(self.path, 'w') as fp:
            self.config.write(fp)

    def validate(self):
        for section, options in self.schema().items():
            for option, label in options.items():
                if self.config.has_option(section, option.lower()) == False:
                    return False
        return True


    def auto(self, option):
        values = {
            'APACHE_RESTART': '$APACHE_BIN/httpd -k restart' if platform.system() == 'Windows' else "apache2 restart",
            'HOSTS_FILE': 'C:/Windows/System32/drivers/etc/hosts' if platform.system() == 'Windows' else "/etc/hosts"
        }

        return values.get(option)