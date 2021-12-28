# :coding: utf-8

# Project Modules
from kid.core.kobject import KObject

# Python Modules
import maya.cmds as cmds


class KAttribute(KObject):
    """ Convience class for query and manipulating node attributes.
    """

    # Class Methods
    @classmethod
    def from_name(cls, node, attr):
        """ Returns a KAttribute from node attribute name.

        Args:
            node(str)
            attr(str)

        Returns:
            KAttribute
        """
        obj = cls()
        obj._value = cmds.getAttr("{}.{}".format(node, attr))

        return obj

    # Object Methods
    def __init__(self):
        self._value = None
        self._type = None
        self._lock = False
        self._hidden = False

    def incoming_connections(self):
        raise NotImplementedError

    def outgoing_connections(self):
        raise NotImplementedError


if __name__ == '__main__':
    pass
