# :coding: utf-8

# Project Modules
from kid.core.kobject import KObject
from kid.core.kvector3 import KVector3
from kid.core.kmatrix4 import KMatrix4
from kid.core.keuler import KEuler

from kid.core.kanim import KAnim

# Python Modules

# Maya Modules
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


class KTransform(KObject):
    """ Class that handles manipulating and querying object transformations.

    References:
        * https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_py_ref_class_open_maya_1_1_m_fn_transform_html
        * https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid
        =Maya_SDK_py_ref_class_open_maya_1_1_m_transformation_matrix_html
        * https://medium.com/swlh/understanding-3d-matrix-transforms-with-pixijs-c76da3f8bd8
    """

    # Static Methods
    @staticmethod
    def get_dag_from_name(name):
        """ Returns MDagPath from scene node name.

        Args:
            name(str): String name of the transformation object.

        Returns:
            OpenMaya.MDagPath()
        """
        selection = OpenMaya.MSelectionList()
        selection.add(name)
        path = OpenMaya.MDagPath()
        selection.getDagPath(0, path)
        return path

    # Class Methods
    @classmethod
    def from_name(cls, name):
        """ Returns new KTransform object from scene node name.

        Args:
            name(str): String name of the transformation object.

        Returns:
            KTransform
        """
        obj = cls()
        obj._name = name
        obj._dag = cls.get_dag_from_name(name)
        obj._fn = OpenMaya.MFnDependencyNode(obj._dag.node())
        return obj

    # Object Methods
    def __init__(self):
        self._name = str()
        self._dag = None
        self._fn = None

    def is_valid(self):
        """ Returns True if the KTransform object has valid components.

        Returns:
            bool
        """
        if self._name and self._dag:
            return True

        return False

    def get_name(self):
        """ Returns the name of the transform.

        Returns:
            str
        """
        return self._name

    def set_dag(self, dag):
        """ Set the current dag path.

        Args:
            dag(OpenMaya.MDagPath):

        Returns:
            None
        """
        self._dag = dag
        return

    def transform(self):
        """ Returns the MFnTransform object from the provided MDagPath.

        References:
            * https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid
            =Maya_SDK_py_ref_class_open_maya_1_1_m_fn_transform_html

        Returns:
            OpenMaya.MFnTransform
        """
        if not self._dag:
            raise RuntimeError("Can't retrieve transform object.")

        return OpenMaya.MFnTransform(self._dag)

    def matrix(self):
        """ Returns the transformation matrix from the Dag Path.

        Returns:
            OpenMaya.MTransformationMatrix
        """
        if not self._dag:
            raise RuntimeError("Can't retrieve matrix object.")

        return self.transform().transformation()

    def world_matrix(self):
        """ Returns the world matrix as KMatrix.

        Returns:
            KMatrix
        """
        attr = self._fn.attribute("worldMatrix")
        plug = OpenMaya.MPlug(self._dag.node(), attr)
        plug = plug.elementByLogicalIndex(0)
        mobject = plug.asMObject()
        data = OpenMaya.MFnMatrixData(mobject)

        return KMatrix4.from_mmatrix(data.matrix())

    def parent_inverse_matrix(self):
        """ Returns the parent inverse matrix as KMatrix.

        Returns:
            KMatrix
        """
        attr = self._fn.attribute("parentInverseMatrix")
        plug = OpenMaya.MPlug(self._dag.node(), attr)
        plug = plug.elementByLogicalIndex(0)
        mobject = plug.asMObject()
        data = OpenMaya.MFnMatrixData(mobject)

        return KMatrix4.from_mmatrix(data.matrix())

    def translation(self, space=OpenMaya.MSpace.kWorld):
        """ Returns the transformation's rotation component as a vector.

        Args:
            space(OpenMaya.MSpace, int)

        Returns:
            OpenMaya.MVector
        """
        return self.matrix().translation(space)

    def get_transform_offset(self, transform):
        """

        Args:
            transform(KTransform)

        Returns:
            KMatrix4
        """
        return self.world_matrix() * transform.world_matrix().inverse()

    def set_translation(self, translation):
        """ Sets the transformation's rotation component in world space.

        Args:
            translation(KVector3, OpenMaya.MVector, list, tuple)

        Returns:
            None
        """
        if isinstance(translation, OpenMaya.MVector):
            self.transform().setTranslation(translation, OpenMaya.MSpace.kWorld)

        elif isinstance(translation, KVector3):
            self.transform().setTranslation(translation.as_mvector(), OpenMaya.MSpace.kWorld)

        elif isinstance(translation, (list, tuple)) and len(translation) == 3:
            self.transform().setTranslation(OpenMaya.MVector(translation[0], translation[1], translation[2]),
                                            OpenMaya.MSpace.kWorld)
        else:
            raise TypeError("Invalid type.")
        return

    def set_rotation(self, rotation, order=0):
        """ Sets the transformation's rotation component in world space.

        Args:
            rotation(KVector3, KEuler, OpenMaya.MEulerRotation, OpenMaya.MQuaternion list, tuple)
            order(int)

        Returns:
            None
        """
        if isinstance(rotation, OpenMaya.MEulerRotation):
            self.transform().setRotation(rotation)

        elif isinstance(rotation, OpenMaya.MQuaternion):
            self.transform().setRotation(rotation, OpenMaya.MSpace.kWorld)

        elif isinstance(rotation, KVector3):
            self.transform().setRotation(OpenMaya.MEulerRotation(rotation.x / KEuler.RADIAN_TO_DEGREES,
                                                                 rotation.y / KEuler.RADIAN_TO_DEGREES,
                                                                 rotation.z / KEuler.RADIAN_TO_DEGREES,
                                                                 order))

        elif isinstance(rotation, KEuler):
            self.transform().setRotation(OpenMaya.MEulerRotation(rotation.x / KEuler.RADIAN_TO_DEGREES,
                                                                 rotation.y / KEuler.RADIAN_TO_DEGREES,
                                                                 rotation.z / KEuler.RADIAN_TO_DEGREES,
                                                                 rotation.order))

        elif isinstance(rotation, (list, tuple)):
            self.transform().setRotation(OpenMaya.MEulerRotation(rotation[0] / KEuler.RADIAN_TO_DEGREES,
                                                                 rotation[1] / KEuler.RADIAN_TO_DEGREES,
                                                                 rotation[2] / KEuler.RADIAN_TO_DEGREES,
                                                                 order),
                                         OpenMaya.MSpace.kWorld)
        else:
            raise TypeError("Invalid type.")
        return

    def set_xform(self, xform):
        """ Sets the transformation matrix from a 16 element list.

        Notes:
            * Using Maya API is 9x faster than Maya Commands, however with Commands the undo stack is more accessible.

        Args:
            xform(list)

        Returns:
            None
        """
        if not isinstance(xform, list) or len(xform) != 16:
            raise TypeError("Invalid type.")

        if self.is_valid():
            cmds.xform(self._name, matrix=xform)

        return

    def set_scale(self):
        raise NotImplementedError


if __name__ == '__main__':
    obj = "pCube1"
    print("Inverse", KTransform.from_name(obj).parent_inverse_matrix())

    pivot = "locator1"

    relative = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, -0.5025402064131258, 0.5026660505043264,
                -0.5051243279494937, 1.0]

    pivot_transform = KTransform.from_name(pivot)
    pivot_matrix = pivot_transform.world_matrix()
    print(pivot_matrix)

    # <KMatrix4x4: [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.5025402064131258,
    # -0.5026660505043264, 0.5051243279494937, 1.0]>
    # <KMatrix4x4: [0.0, -1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.5025402064131258,
    # -0.5026660505043264, 0.5051243279494937, 1.0]>

    # Decompose
    print(pivot_matrix[0][0])
