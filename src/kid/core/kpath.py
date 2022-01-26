# :coding: utf-8

# Project Modules
from kid.core.kobject import KObject

# Python Modules
import os
import sys
from copy import deepcopy


class KPath(KObject):
    """ A convience class that handles creating and manipulating paths.

    Args:
        path(str)
    """
    TYPE_NONE = "None"
    TYPE_FILE = "File"
    TYPE_DIRECTORY = "Directory"

    @staticmethod
    def from_user():
        return KPath(os.path.expanduser('~'))

    def __init__(self, path):
        self._path = os.path.abspath(path)

    def __str__(self):
        kwargs = {
            self.type(): self.is_valid(),
            "Path"     : self._path
            }
        return self.str_formatter(**kwargs)

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("Invalid index provided.")

        if self._path:
            return self.split()[item]
        raise IndexError("List index out of range.")

    def __add__(self, other):
        if isinstance(other, str):
            return KPath(os.path.join(self._path, other))
        elif isinstance(other, KPath):
            return KPath(os.path.join(self._path, other.path()))
        raise TypeError("Invalid type provided.")

    def __radd__(self, other):
        if isinstance(other, str):
            return KPath(os.path.join(other, self._path))
        elif isinstance(other, KPath):
            return KPath(os.path.join(other.path(), self._path))
        raise TypeError("Invalid type provided.")

    def __iadd__(self, other):
        if isinstance(other, (str, KPath)):
            self.append(other)
            return self

        raise TypeError("Invalid type provided.")

    def __sub__(self, other):
        if isinstance(other, (str, KPath)):
            _copy = deepcopy(self)
            _copy.remove(other)
            return _copy

        raise TypeError("Invalid type provided.")

    def __isub__(self, other):
        if isinstance(other, (str, KPath)):
            self.remove(other)
            return self

        raise TypeError("Invalid type provided.")

    def path(self):
        return self._path

    def as_str(self):
        return self._path

    def type(self):
        """ Returns the path type.

        Returns:
            str
        """
        if self._path:
            if self.extension():
                return KPath.TYPE_FILE
            else:
                return KPath.TYPE_DIRECTORY

        return KPath.TYPE_NONE

    def is_valid(self):
        if self.is_file() or self.is_directory():
            return True

        return False

    def is_file(self):
        return os.path.isfile(self._path)

    def is_directory(self):
        return os.path.isdir(self._path)

    def base(self):
        """ Returns the current base name as a KPath object.

        Returns:
            str
        """
        if self._path:
            return os.path.basename(self._path)
        return str()

    def directory(self):
        """ Returns the current directory as a KPath object.

        Returns:
            KPath
        """
        if self._path:
            return KPath(os.path.dirname(self._path))
        return KPath(str())

    def extension(self):
        """ Returns the file path extension if there is one.

        Returns:
            str
        """
        if self._path:
            filename, extension = os.path.splitext(self._path)
            return extension
        return str()

    def append(self, item):
        """ Appends the a str item or a KPath to the current path.

        Args:
            item(str, KPath)

        Returns:
            self
        """
        if isinstance(item, str):
            pass
        elif isinstance(item, KPath):
            item = item.path()
        else:
            raise TypeError("Invalid type.")

        if self._path:
            self._path = os.path.join(self._path, item)
        else:
            self._path = os.path.abspath(item)
        return self

    # FIXME: This method is not 100% bulletproof
    def remove(self, item):
        """ Removes an item from the path.

        Args:
            item(str, KPath)

        Returns:
            None
        """
        if isinstance(item, str):
            pass
        elif isinstance(item, KPath):
            item = item.path()
        else:
            raise TypeError("Invalid type.")

        if self._path:
            if "/" in item or "\\" in item:
                path = os.path.normpath(item)
                query = path.split(os.sep)
                split = self.split()

                for q in query:
                    if q in split:
                        split.remove(q)

                self._path = os.path.join(*split)

            else:
                split = self.split()

                if item in split:
                    split.remove(item)
                    self._path = os.path.join(*split)
        return

    def filename(self):
        """ Returns the current file name if there is one.

        Returns:
            str
        """
        if self._path:
            base = os.path.basename(self._path)
            filename, extension = os.path.splitext(base)
            return filename
        return str()

    def split(self):
        """ Returns the current path as a list.

        Returns:
            list
        """
        if self._path:
            path = os.path.normpath(self._path)
            return path.split(os.sep)
        return list()


if __name__ == '__main__':
    _test = KPath.from_user()
    print(_test)
    _test -= "core"
    print(_test)
