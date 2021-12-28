# :coding: utf-8

# Project Modules
from kid.core.kmatrix import KMatrix
from kid.core.kvector3 import KVector3
from kid.core.keuler import KEuler

# Python Modules

# Maya Modules
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


class KMatrix4(KMatrix):
    # Static Methods
    @staticmethod
    def get_raw_origin():
        """
        Returns:
            list
        """
        return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]

    @staticmethod
    def xform_to_mmatrix(xform):
        """ Returns a MMatrix object from a xform list.

        Args:
            xform(list): 16 element list

        Returns:
            OpenMaya.MMatrix
        """
        matrix = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil().createMatrixFromList(xform, matrix)
        return matrix

    @staticmethod
    def mmatrix_to_list(matrix):
        """ Returns a 4x4 matrix from MMatrix object.

        Args:
            matrix(OpenMaya.MMatrix)

        Returns:
            list
        """
        data = list()

        for row_index in range(4):
            row = list()

            for column_index in range(4):
                value = matrix(row_index, column_index)
                row.append(value)

            data.append(row)

        return data

    # Class Methods
    @classmethod
    def decompose_matrix(cls, matrix):
        """ Returns a xform matrix decomposition from a MMatrix.

        References:
            * https://soup-dev.websitetoolbox.com/post/decompose-matrix-and-extract-rotation-values-6406381
            * https://stackoverflow.com/questions/1996957/conversion-euler-to-matrix-and-matrix-to-euler
            * https://bindpose.com/maya-matrix-based-functions-part-1-node-based-matrix-constraint/

        Args:
            matrix(list)

        Returns:
            tuple
        """
        # Get Axes
        x_axis = KVector3(matrix[0][0], matrix[0][1], matrix[0][2])
        y_axis = KVector3(matrix[1][0], matrix[1][1], matrix[1][2])
        z_axis = KVector3(matrix[2][0], matrix[2][1], matrix[2][2])

        # Get Translation
        translation = KVector3(matrix[3][0], matrix[3][1], matrix[3][2])

        # # Get Rotation Quaternion
        # quaternion = None

        # Get Rotation Euler
        euler = KEuler.from_matrix(matrix)

        # Get Scale
        scale = KVector3(x_axis.length(), y_axis.length(), z_axis.length())

        return translation, euler, scale

    @classmethod
    def from_xform(cls, xform):
        """ Returns a new KMatrix object from a xform list.

        Args:
            xform(list): 16 element list

        Returns:
            KMatrix
        """
        if len(xform) != 16:
            raise TypeError("Invalid xform length.")

        obj = cls()
        matrix = [xform[x:x + 4] for x in range(0, len(xform), 4)]
        obj.set_data(matrix)
        return obj

    @classmethod
    def from_mmatrix(cls, matrix):
        """ Returns KMatrix object from OpenMaya.MMatrix

        Args:
            matrix(OpenMaya.MMatrix)

        Returns:
            KMatrix
        """
        obj = cls()
        obj.set_data(cls.mmatrix_to_list(matrix))
        return obj

    @classmethod
    def get_relative_from_node(cls, a, b):
        """ Returns a relative MMatrix object from two transforms.

        Args:
            a(str): String name of child transform node.
            b(str): String name of parent transform node.

        Returns:
            OpenMaya.MMatrix
        """
        node_matrix = cls.xform_to_mmatrix(cmds.xform(a, query=True, matrix=True, worldSpace=True))
        parent_matrix = cls.xform_to_mmatrix(cmds.xform(b, query=True, matrix=True, worldSpace=True))
        return node_matrix * parent_matrix.inverse()

    # Object Methods
    def __init__(self):
        KMatrix.__init__(self)

        self.set_data(self.get_raw_origin())

    def as_mmatrix(self):
        """ Returns a MMatrix object.

        Returns:
            OpenMaya.MMatrix
        """
        return self.xform_to_mmatrix(self.as_xform())

    def as_xform(self):
        """ Returns a 16 element list of floats.

        Returns:
            list
        """
        result = list()

        for row in range(4):
            for column in range(4):
                result.append(self[row][column])

        return result

    def decompose(self):
        """

        Returns:
            tuple
        """
        return self.decompose_matrix(self._data)

    def inverse(self):
        """

        Returns:
            KMatrix
        """
        obj = KMatrix4()
        obj.set_data(self.get_matrix_inverse(list(self.data())))
        return obj


if __name__ == '__main__':
    _obj = KMatrix4() + KMatrix4()

    #_obj.set_data([[0.0, -1.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.5025402064131258, -0.5026660505043264, 0.5051243279494937, 1.0]])

    print(_obj.as_list())
    for x in _obj.decompose():
        print(x)
