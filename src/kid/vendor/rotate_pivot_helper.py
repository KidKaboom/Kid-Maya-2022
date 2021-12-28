# :coding: utf-8

# Project Modules
from src.kid import KObject, KMatrix4


# Python Modules


class RotatePivotHelper(KObject):
    """

    References:
        * https://charliebanks3d.wordpress.com/2018/05/02/rigging-with-matrices-parenting/

    """

    # Static Methods
    @staticmethod
    def get_offset(parent, child):
        """ Returns an update_offset matrix from two matrics.

        Args:
            parent(KTransform)
            child(KTransform)

        Returns:
            KMatrix4
        """
        return KMatrix4.from_mmatrix(child.world_matrix() * parent.world_matrix().inverse())

    @staticmethod
    def align(parent, child, offset):
        """

        Args:
            parent(KMatrix4)
            child(KMatrix4)
            offset(KMatrix4)

        Returns:
            None
        """
        return

    # Object Methods
    def __init__(self):
        self._pivot = str()

    def set_pivot(self, pivot):
        """ Set the current pivot node.

        Args:
            pivot(str): Name of the pivot transform.

        Returns:
            None
        """
        self._pivot = pivot
        return


if __name__ == '__main__':
    pass
