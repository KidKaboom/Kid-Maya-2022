# :coding: utf-8

# Project Modules
from kid.core.kobject import KObject

# Python Modules

# Maya Modules
import maya.cmds as cmds


class KKeyTangent(KObject):
    """

    """

    def __init__(self):
        self._in_x = None
        self._in_y = None
        self._in_angle = None
        self._in_type = None
        self._in_weight = None

        self._out_x = None
        self._out_y = None
        self._out_angle = None
        self._out_type = None
        self._out_weight = None


class KKeyFrame(KObject):
    """

    """

    # Class Methods
    @classmethod
    def keyframe_from_name(cls, node, attr, time):
        """ Returns a KKeyframe object from node and attribute name.

        Args:
            node(str)
            attr(str)
            time(float)

        Returns:
            KObject
        """
        obj = cls()
        query = "{}.{}".format(node, attr)
        obj.time = time
        obj.value = cmds.getAttr(query, time=time)
        return obj

    # Object Methods
    def __init__(self):
        self._time = None
        self._value = None

        self._tangent = KKeyTangent()

    def __getitem__(self, item):
        return [self._time, self._value][item]

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        return

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        return


if __name__ == '__main__':
    pass
