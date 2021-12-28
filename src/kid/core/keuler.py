# :coding: utf-8

# Project Modules
from kid.core.kobject import KObject

# Python Modules
import math


class KEuler(KObject):
    """ Class that handles manageing and manipulating euler rotations.

    References:
        * https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_py_ref_class_open_maya_1_1_m_euler_rotation_html

    """
    XYZ = 0
    XZY = 3
    YXZ = 4
    YZX = 1
    ZXY = 2
    ZYX = 5

    RADIAN_TO_DEGREES = 57.2957795

    @classmethod
    def from_matrix(cls, matrix):
        """ Returns a rotation matrix4x4 from a transformation matrix.

        References:
            * https://forums.cgsociety.org/t/4x4-matrix-to-transform-values/1743190/9

        Args:
            matrix(list): Matrix 4x4

        Returns:
            KEuler
        """
        obj = cls()

        obj.x = math.atan2(matrix[1][2], matrix[2][2]) * cls.RADIAN_TO_DEGREES
        obj.y = -math.asin(matrix[0][2]) * cls.RADIAN_TO_DEGREES
        obj.z = math.atan2(matrix[0][1], matrix[0][0]) * cls.RADIAN_TO_DEGREES

        return obj

    @classmethod
    def from_kvector(cls, kvector, order=0):
        """ Returns a KEuler roatation from KVector3

        Args:
            kvector(KVector3)
            order(int)

        Returns:
            KEuler
        """
        obj = cls()
        obj.x = kvector.x
        obj.y = kvector.y
        obj.z = kvector.z
        obj.order = order
        return obj

    @classmethod
    def from_iter(cls, value, order=0):
        """ Returns a KEuler roatation from KVector3

        Args:
            value(list, tuple)
            order(int)

        Returns:
            KEuler
        """
        if len(value) != 3:
            raise TypeError("Invalid type.")

        obj = cls()
        obj.x = value[0]
        obj.y = value[1]
        obj.z = value[2]
        obj.order = order
        return obj

    # Object Methods
    def __init__(self, x=0.0, y=0.0, z=0.0, order=0):
        """
        Args:
            x(float):  X rotation in radians
            y(float):  Y rotation in radians
            z(float):  Z rotation in radians
            order(int): Rotation order
        """
        self._x = float(x),
        self._y = float(y),
        self._z = float(z),
        self._order = order

    def __str__(self):
        return self.str_formatter((self.x, self.y, self.z))

    def __repr__(self):
        return self.x, self.y, self.z

    def __getitem__(self, item):
        result = [self.x, self.y, self.z]
        return result[item]

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = float(value)
        return

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = float(value)
        return

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = float(value)
        return

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        if not isinstance(value, int):
            raise TypeError("Invalid type")
        elif 0 > value > 5:
            raise IndexError

        self._order = value
        return

    def as_list(self):
        return list(self)


if __name__ == '__main__':
    pass
