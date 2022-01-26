# :coding: utf-8

# Project Modules
from kid.core import KObject
from kid.io.kio import KIO

# Python Modules


class Kcsv(KIO):
    def extension(self):
        return ".csv"

    def write_handler(self, *args, **kwargs):
        pass

    def read_handler(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    pass

