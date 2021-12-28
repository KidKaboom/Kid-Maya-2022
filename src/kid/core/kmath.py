# :coding: utf-8

# Project Modules

# Python Modules
import math


class KMath:
    """ Utility class with methods commonly used in 3D productions.
    """

    @classmethod
    def clamp(cls, value, _min, _max):
        """ Returns a weight within a specified range.

        Args:
            value(int, float)
            _min(int, float)
            _max(int, float)

        Returns:
            float
        """
        return max(min(float(value), float(_max)), float(_min))

    @classmethod
    def set_range(cls, value, old_min, old_max, new_min, new_max):
        """ Returns a value from one range, and map them into another range.

        Args:
            value(int, float)
            old_min(int, float)
            old_max(int, float)
            new_min(int, float)
            new_max(int, float)

        Returns:
            float
        """
        value = float(value)
        old_min = float(old_min)
        old_max = float(old_max)
        new_min = float(new_min)
        new_max = float(new_max)
        return new_min + (((value - old_min) / (old_max - old_min)) * (new_max - new_min))


if __name__ == '__main__':
    pass
