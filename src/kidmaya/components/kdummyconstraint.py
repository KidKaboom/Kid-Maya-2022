# :coding: utf-8

# Project Modules
from kid.core import KObject, KTransform

# Python Modules

# Maya Modules
import maya.cmds as cmds


class KDummyConstraint(KObject):
    """ Class that handles creating a constraint between two transforms stored only in memory.

    References:
        * https://charliebanks3d.wordpress.com/2018/05/02/rigging-with-matrices-parenting/

    Args:
        parent(KTransform):     Parent transform node.
        child(KTransform):      Child transform node.
        offset(bool):           Maintain update_offset between parent and child.
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
        return child.world_matrix() * parent.world_matrix().inverse()

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

    # Class Methods
    @classmethod
    def from_name(cls, parent, child, offset=False):
        """ Convenice method to create KDummyConstraint from string names.

        Args:
            parent(str): Name of the parent transform node.
            child(str): Name of the child transform node.
            offset(bool): Maintain update_offset between parent and child.

        Returns:
            KDummyConstraint
        """
        obj = cls()
        obj.set_parent(KTransform.from_name(parent))
        obj.set_child(KTransform.from_name(child))
        obj.set_maintain_offset(offset)
        return obj

    # Object Methods
    def __init__(self, parent=None, child=None, offset=False):
        self._parent = parent
        self._child = child
        self._maintain_offset = offset
        self._offset = None

        self.update_offset()

    def __str__(self):
        parent = self._parent.get_name() if self._parent else None
        child = self._child.get_name() if self._child else None
        return self.str_formatter(parent, child, self._maintain_offset)

    def is_valid(self):
        """ Returns true if has valid components.

        Returns:
            bool
        """
        if isinstance(self._parent, KTransform) and isinstance(self._child, KTransform):
            return True

        return False

    def set_parent(self, parent):
        """ Set the current parent transform node.

        Args:
            parent(KTransform): Name of the pivot transform.

        Returns:
            None
        """
        if not isinstance(parent, KTransform):
            raise TypeError("Invalid type.")

        self._parent = parent
        return

    def set_child(self, child):
        """ Set the current child transform node.

        Args:
            child(KTransform): Name of the pivot transform.

        Returns:
            None
        """
        if not isinstance(child, KTransform):
            raise TypeError("Invalid type.")

        self._child = child
        return

    def set_maintain_offset(self, offset):
        """ Set to maintain the current update_offset.

        Args:
            offset(bool)

        Returns:
            None
        """
        if not isinstance(offset, bool):
            raise TypeError("Invalid type.")

        self._maintain_offset = offset
        self.update_offset()
        return

    def offset(self):
        """ Returns the current offset if there is one.

        Returns:
            KMatrix4
        """
        return self._offset

    def update_offset(self):
        """ Recalculates update_offset.

        Returns:
            None
        """
        if self.is_valid() and self._maintain_offset:
            self._offset = self.get_offset(self._parent, self._child)
        return

    def update(self):
        """ Calulcates the new position of the child position and update.

        Returns:
            None
        """
        if self.is_valid():
            # Get Matrics
            parent_matrix = self._parent.world_matrix()
            child_matrix = self._child.parent_inverse_matrix()

            # Mutliply Matrices
            if self._maintain_offset:
                mult = self._offset * parent_matrix * child_matrix
            else:
                mult = parent_matrix * child_matrix

            # Decompose Matrix Sum
            translation, euler, scale = mult.decompose()

            # Update Transformation
            
            # This code works, but I want to use the API instead - for reference.
            cmds.setAttr("{}.tx".format(self._child.get_name()), translation[0])
            cmds.setAttr("{}.ty".format(self._child.get_name()), translation[1])
            cmds.setAttr("{}.tz".format(self._child.get_name()), translation[2])

            # cmds.setAttr("{}.rx".format(self._child.get_name()), euler[0])
            # cmds.setAttr("{}.ry".format(self._child.get_name()), euler[1])
            # cmds.setAttr("{}.rz".format(self._child.get_name()), euler[2])

            # Api version
            # self._child.set_translation(translation)
            # self._child.set_rotation(euler)
        return


if __name__ == '__main__':
    _parent = "locator1"
    _child = "pCube1"

    _constraint = KDummyConstraint.from_name(_parent, _child, True)
    # print(_constraint)
    # print(_constraint.offset())
    cmds.setAttr("{}.rz".format(_parent), -45)
    _constraint.update()
