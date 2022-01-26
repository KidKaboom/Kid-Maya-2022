# :coding: utf-8

# Project Modules
from kid.core import KObject
from kid.io.kio import KIO

# Python Modules


class Kxml(KIO):
    def extension(self):
        return ".xml"

    def write_handler(self, *args, **kwargs):
        pass

    def read_handler(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    pass

