# :coding: utf-8

# Project Modules

# Python Modules
from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty, abstractstaticmethod


class KAbstractTool(ABC):
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

    @abstractstaticmethod
    def show(*args, **kwargs):
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    pass
