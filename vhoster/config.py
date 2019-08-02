import os
import json
from copy import deepcopy
from .helpers import *
from .errors import InvalidConfigError


class Config:
    """Configuration Driver

    Keyword Arguments:
        path {str} -- path to data store file (default: {''})
    """

    def __init__(self, path=''):
        self.__path = path
        self.__data = {}
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
            str
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

    def set(self, key, value, create=True):
        """Set value of given key

        Arguments:
            key {str} -- key using dot notation
            value {mixed} -- key value
            create {bool} -- allow creation of new key
        """
        nodes = key.split('.')
        data = self.__data

        for i, node in enumerate(nodes):
            if isinstance(data, dict):
                if i + 1 == len(nodes) and (node in data.keys() or create):
                    data[node] = value
                    break
                else:
                    if node in data.keys():
                        data = data[node]
                    elif create:
                        data[node] = value
                        break

        self.save()

    def rem(self, key):
        """Remove value by key, if exists

        Arguments:
            key {str} -- key using dot notation
        """
        nodes = key.split('.')
        data = self.__data

        for i, node in enumerate(nodes):
            if isinstance(data, dict):
                if i + 1 == len(nodes) and node in data.keys():
                    del data[node]
                    break
                else:
                    if node in data.keys():
                        data = data[node]
                        break

        self.save()

    def load(self):
        """Load data from file, if path is defined"""
        try:
            if self.__path:
                with open(self.__path, 'r') as f:
                    self.__data = json.load(f)
        except Exception as err:
            raise InvalidConfigError(str(err))

    def save(self):
        """Save data to file, if file is defined"""
        if self.__path:
            with open(self.__path, 'w+') as f:
                json.dump(self.__data, f, indent=4)
