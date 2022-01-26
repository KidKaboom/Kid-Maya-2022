# :coding: utf-8

# Project Modules
from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty, abstractstaticmethod


# Python Modules


class KMTool(ABC):
    @abstractstaticmethod
    def name():
        raise NotImplementedError

    @abstractstaticmethod
    def title():
        raise NotImplementedError

    @abstractstaticmethod
    def description():
        raise NotImplementedError

    @abstractstaticmethod
    def icon():
        raise NotImplementedError

    @classmethod
    def do_it(cls, *args, **kwargs):
        try:
            obj = cls(*args, **kwargs)
            obj.show()
        except Exception as _error:
            raise RuntimeError(_error)
        return

    @classmethod
    def register(cls):
        return

    def __init__(self, *args, **kwargs):
        pass

    def show(self, *args, **kwargs):
        raise NotImplemented


if __name__ == '__main__':
    pass
