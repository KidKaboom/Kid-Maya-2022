# :coding: utf-8

# Project Modules
from kid.core import KDebug

# Python Modules
from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty, abstractstaticmethod

# Maya Modules
import maya.cmds as cmds


class KMCommand(ABC):
    @staticmethod
    def name():
        raise NotImplementedError

    @staticmethod
    def title():
        raise NotImplementedError

    @staticmethod
    def description():
        raise NotImplementedError

    @staticmethod
    def icon():
        raise NotImplementedError

    @classmethod
    def do_it(cls, *args, **kwargs):
        cmds.undoInfo(openChunk=True)

        try:
            cls(*args, **kwargs)
        except Exception as _error:
            KDebug.error(_error)
            raise
        finally:
            cmds.undoInfo(closeChunk=True)

        return

    @classmethod
    def register(cls):
        raise NotImplemented


if __name__ == '__main__':
    _test = KMCommand()
