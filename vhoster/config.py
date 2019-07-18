import os, json
from .helpers import *

class Config:

    _filepath = ''
    _synced = False
    _data = None

    def __init__(self, path):            
        self._filepath = path
        self.load()

    def __getattr__(self, name):
        return self.get(name)

    def install(self):
        default = {
            "tld": "test",
            "dns": {
                "file": "C:/Windows/System32/drivers/etc/hosts"
            },
            "apache": {
                "bin": "C:/Xampp/apache/bin/httpd.exe",
                "conf": "C:/Xampp/apache/conf/extra/httpd-vhosts.conf"
            },
            "collection": [],
            "sites": []
        }
        
    def get(self, key, default=None):
        nodes = key.split('.')
        data = self._data

        for i, node in enumerate(nodes):
            if isinstance(data, dict):
                if i + 1 == len(nodes):
                    return data[node]
                else:                
                    if node in data.keys():
                        data = data[node]
                    else:
                        break
            
        return default


    def set(self, key, value):
        nodes = key.split('.')
        data = self._data

        for i, node in enumerate(nodes):
            if isinstance(data, dict):
                if i + 1 == len(nodes):
                    data[node] = value
                    self._synced = False
                    self.save()
                    return True
                else:                
                    if node in data.keys():
                        data = data[node]                        
                    else:
                        break
            
        return False

    def load(self, force=False):
        if (not self._synced) or force:
            with open(self._filepath, 'r') as f:
                self._data = json.load(f)
                self._synced = True

    def save(self, force=False):
        if (not self._synced) or force:
            with open(self._filepath, 'w+') as f:
                json.dump(self._data, f, indent=4)
            
            self.load()


