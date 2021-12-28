# :coding: utf-8

# Project Modules
from kid.core.kobject import KObject

# Python Modules
import math

# Maya Modules
import maya.OpenMaya as OpenMaya


class KVector3(KObject):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)

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

    def __str__(self):
        return self.str_formatter((self.x, self.y, self.z))

    def __repr__(self):
        return self.x, self.y, self.z

    def __getitem__(self, item):
        result = [self.x, self.y, self.z]
        return result[item]

    def __add__(self, other):
        if isinstance(other, float):
            return KVector3(self.x + other, self.y + other, self.z + other)

        elif isinstance(other, int):
            other = float(other)
            return KVector3(self.x + other, self.y + other, self.z + other)

        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ArithmeticError("Invalid type.")

            return KVector3(self.x + other[0], self.y + other[1], self.z + other[2])

        elif isinstance(other, (KVector3, OpenMaya.MMatrix)):
            return KVector3(self.x + other.x, self.y + other.y, self.z + other.z)

        raise ArithmeticError("Invalid type.")
    
    def __sub__(self, other):
        if isinstance(other, float):
            return KVector3(self.x - other, self.y - other, self.z - other)

        elif isinstance(other, int):
            other = float(other)
            return KVector3(self.x - other, self.y - other, self.z - other)

        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ArithmeticError("Invalid type.")

            return KVector3(self.x - other[0], self.y - other[1], self.z - other[2])

        elif isinstance(other, (KVector3, OpenMaya.MMatrix)):
            return KVector3(self.x - other.x, self.y - other.y, self.z - other.z)

        raise ArithmeticError("Invalid type.")
    
    def __mul__(self, other):
        if isinstance(other, float):
            return KVector3(self.x * other, self.y * other, self.z * other)

        elif isinstance(other, int):
            other = float(other)
            return KVector3(self.x * other, self.y * other, self.z * other)

        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ArithmeticError("Invalid type.")

            return KVector3(self.x * other[0], self.y * other[1], self.z * other[2])

        elif isinstance(other, (KVector3, OpenMaya.MMatrix)):
            return KVector3(self.x * other.x, self.y * other.y, self.z * other.z)

        raise ArithmeticError("Invalid type.")
    
    def __div__(self, other):
        if isinstance(other, float):
            return KVector3(self.x / other, self.y / other, self.z / other)

        elif isinstance(other, int):
            other = float(other)
            return KVector3(self.x / other, self.y / other, self.z / other)

        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ArithmeticError("Invalid type.")

            return KVector3(self.x / other[0], self.y / other[1], self.z / other[2])

        elif isinstance(other, (KVector3, OpenMaya.MMatrix)):
            return KVector3(self.x / other.x, self.y / other.y, self.z / other.z)

        raise ArithmeticError("Invalid type.")

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def length(self):
        """ Returns the length of the Vector.

        Returns:
            float
        """
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normal(self):
        raise NotImplementedError

    def normalize(self):
        raise NotImplementedError

    def angle(self):
        raise NotImplementedError

    def as_list(self):
        """ Returns a list of float xyz values.

        Returns:
            list
        """
        return list(self)

    def as_mvector(self):
        """ Returns an OpenMaya.MVector object.

        Returns:
            OpenMaya.MVector
        """
        return OpenMaya.MVector(self.x, self.y, self.z)


if __name__ == '__main__':
    _obj = KVector3() + KVector3(6, 0, 9)
    print(_obj.length())
    print(_obj.as_list())
