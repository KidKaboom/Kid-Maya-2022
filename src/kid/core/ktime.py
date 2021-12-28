# :coding: utf-8

# Project Modules
from kobject import KObject

# Python Modules
from time import time


class KTime(KObject):
    def __init__(self):
        self._fps = None

    def as_timecode(self):
        raise NotImplemented


class KTimecode(KObject):
    def __init__(self):
        pass

    def as_time(self):
        raise NotImplemented


if __name__ == '__main__':
    pass
