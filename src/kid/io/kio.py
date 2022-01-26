# :coding: utf-8

# Project Modules
from kid.core import KObject, KPath
from kid.__version__ import VERSION

# Python Modules
import os
import getpass
import time
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty, abstractstaticmethod


class KIORoot(KObject):
    def __init__(self):
        self.path = str()
        self.version = VERSION
        self.user = getpass.getuser()
        self.date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.type = str()
        self.extension = str()

    def __str__(self):
        return self.str_formatter(**self.as_dict())


class KIO(ABC):
    """ Abstract base class that handles IO file operations.

    Args:
        filepath(str, KPath): The str name or object pointing to the file path.
        mode(str): The mode of the file operation. Read, Write or Debug.
    """
    MODE_READ = "r"
    MODE_WRITE = "w"
    MODE_DEBUG = "d"
    MODES = [MODE_READ, MODE_WRITE, MODE_DEBUG]

    @classmethod
    def read(cls, filepath):
        """ Returns data read from a file path.

        Args:
            filepath(str, KPath)

        Returns:
            KIO
        """
        with cls(filepath, KIO.MODE_READ) as reader:
            pass
        return reader

    @classmethod
    def write(cls, filepath, data):
        """ Write date to filepath.

        Args:
            filepath(str, KPath)
            data(data)

        Returns:
            KIO
        """
        with cls(filepath, KIO.MODE_WRITE) as writer:
            writer.data = data
        return writer

    def __init__(self, filepath, mode):

        self._filepath = None
        self._mode = None
        self._file = None
        self.root = KIORoot()
        self.data = None
        self._exception = list()
        self._handlers = dict()

        if isinstance(filepath, str):
            self._filepath = KPath(filepath)
        elif isinstance(filepath, KPath):
            self._filepath = filepath
        else:
            raise TypeError("Invalid file path type.")

        if self._filepath.extension() != self.extension():
            raise TypeError("Invalid extension type.")
        if isinstance(mode, str) and mode in KIO.MODES:
            self._mode = mode
        else:
            raise TypeError("Invalid mode type.")

    @abstractmethod
    def extension(self):
        raise NotImplementedError

    @abstractmethod
    def write_handler(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def read_handler(self, *args, **kwargs):
        raise NotImplementedError

    def __enter__(self):
        if self._mode == KIO.MODE_READ:
            self._file = open(self._filepath.as_str(), KIO.MODE_READ)
            self.read_handler()
        elif self._mode == KIO.MODE_WRITE:
            self._file = open(self._filepath.as_str(), KIO.MODE_WRITE)
            self.root.extension = self.extension()
            self.root.path = self.path()
        elif self._mode == KIO.MODE_DEBUG:
            pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._mode == KIO.MODE_READ:
            pass
        elif self._mode == KIO.MODE_WRITE:
            self.write_handler()
        elif self._mode == KIO.MODE_DEBUG:
            pass

        if self._file:
            self._file.close()
        return

    def path(self):
        """ Returns the current file path.

        Returns:
            str
        """
        return self._filepath.as_str()

    def file(self):
        """ Returns the current file object.

        Returns:
            object
        """
        return self._file

    def set_header(self, **kwargs):
        """ Set the current root header properties.

        Args:
            **kwargs

        Returns:
            None
        """
        for kwarg in kwargs:
            if hasattr(self.root, kwarg):
                setattr(self.root, kwarg, kwargs[kwarg])
        return


if __name__ == '__main__':
    _root = KIORoot()
    print(_root.as_dict())
