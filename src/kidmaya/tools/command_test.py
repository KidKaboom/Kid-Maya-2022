# :coding: utf-8

# Project Modules
from kidmaya.core import KMCommand

# Python Modules


class CommandTest(KMCommand):
    @staticmethod
    def name():
        return "testCmd"

    @staticmethod
    def title():
        return "Test"

    @staticmethod
    def description():
        return "This is a test command."

    @staticmethod
    def icon():
        return ":/mayaIcon.png"

    def __init__(self, *args, **kwargs):
        print(args, kwargs)


if __name__ == '__main__':
    _test = CommandTest()
    import dis
    # print(dis.dis(CommandTest.do_it))
    eval("CommandTest.do_it")

