import os
import json
from copy import deepcopy
from vhoster.helpers import *


class Config:
    """Configuration Driver Class"""

    # Path to data store file
    __path = ''

    # Config data container
    __data = None

    def __init__(self, path=''):
        """Initialize configuration driver instance

        Keyword Arguments:
            path {str} -- path to data store file (default: {''})
        """
        self.__path = path
        self.load()

    def __repr__(self):
        """Return the canonical representation of this object
        
        Returns:
            str
        """
        return '%s(path=%s)' % (self.__class__.__name__, repr(self.__path))

    def __str__(self):
        """Return the string representation of this object
        
        Returns:
            str
        """
        return str(self.__data)

    @property
    def path(self):
        """Get the path of data store file
        
        Returns:
            [type] -- [description]
        """
        return self.__path

    def get(self, key='', default=None, copy=False):
        """Get value of given key

        Keyword Arguments:
            key {str} -- key using dot notation (default: {''})
            default {mixed} -- default value if key does not exist (default: {None})
            copy {bool} -- create a copy of the value (to break memory refence) (default: {False})

        Returns:
            mixed
        """
        return dot_get(self.__data, key, default, copy)

    def set(self, key, value):
        """Set value of given key, create if not exists

        Arguments:
            key {str} -- key using dot notation
            value {mixed} -- key value
        """
        nodes = key.split('.')
        data = self.__data

        for i, node in enumerate(nodes):
            if isinstance(data, dict):
                if i + 1 == len(nodes):
                    data[node] = value
                else:
                    if node in data.keys():
                        data = data[node]
                    else:
                        data[node] = value

        self.save()

    def load(self):
        """Load data from file, if path is defined"""
        if self.__path:
            with open(self.__path, 'r') as f:
                self.__data = json.load(f)

    def save(self):
        """Save data to file, if file is defined"""
        if self.__path:
            with open(self.__path, 'w+') as f:
                json.dump(self.__data, f, indent=4)
