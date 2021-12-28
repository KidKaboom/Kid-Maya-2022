# :coding: utf-8

# Project Modules
from src.kid.core.ktransform import KTransform

# Python Modules
import math
import gc

# Maya Modules
import maya.cmds as cmds
import maya.mel as mel


class TempPivot(object):
    """ Class that handles the creation and management of temporary rotation pivots.

    Class Args:
        WORLDSPACE(int)
        CACHE(dict):    {node: (rotatePivot, manipOrientation)}

    Args:
        transforms(list)
        pivot(str)
    """
    WORLDSPACE = 3
    CACHE = dict()

    # Static Methods
    @staticmethod
    def update_context_tool():
        """ Change the current context tool to manipulate the pivot.

        Returns:
            None
        """
        cmds.setToolTo('moveSuperContext')
        cmds.ctxEditMode()
        return

    @staticmethod
    def manip_pivot_orientation():
        """ Returns component pivot orientation in world-space.

        Returns:
            list(float)
        """
        return cmds.manipPivot(query=True, ori=True)[0]

    @staticmethod
    def clear_cache():
        """ Clears the cache.

        Returns:
            None
        """
        TempPivot.CACHE = dict()
        gc.collect()
        return

    # Object Methods
    def __init__(self):
        self.transforms = list()
        self.pivot = str()
        self._relative_matrices = list()

    # Private Methods
    def _set_temp_pivot(self):
        return

    def _align_pivot_to_parent(self):
        node = self.transforms[-1]
        transform = KTransform(node)

        world_matrix = transform.world_matrix()
        rotate_pivot = self._rotate_pivot()

        cmds.xform(self.pivot, zeroTransformPivots=True)

        # FIXME: Sure this is more complicated than my initial thoughts. Need to test and fix.
        # o__0_____0_0_0_____1___O__0__O_0___l____l_O = o___1____o_1_O__O___0____0(
        #     world_matrix).o___O__0_____1___O_____1_____0

        translation = transform.translation()
        cmds.xform(self.pivot, translation=[translation.x,
                                            translation.y,
                                            translation.z
                                            ],
                   worldSpace=True)

        # MTransformationMatrix.eulerRotation()
        #euler_rotation = o___1____o_1_O__O___0____0(world_matrix).eulerRotation(0)

        euler_rotation = transform.matrix().eulerRotation(0)

        cmds.xform(self.pivot, rotation=[math.degrees(euler_rotation.x),
                                         math.degrees(euler_rotation.y),
                                         math.degrees(euler_rotation.z)],
                   worldSpace=False)

        cmds.xform(self.pivot, rotatePivot=rotate_pivot)
        cmds.xform(self.pivot, scalePivot=rotate_pivot)
        return

    def _center_pivot(self):
        return

    def _rotate_pivot(self):
        """ Returns the temporary rotate pivot as a list.

        Returns:
            List(float)
        """
        if self.pivot:
            return cmds.xform(self.pivot, query=True, rotatePivot=True)

        return list()

    def _add_to_cache(self, node):
        """
        Args:
            node (str): name of the node to append to the cache.

        Returns:
            None
        """
        TempPivot.CACHE[node] = (self._rotate_pivot(), self.manip_pivot_orientation())
        return

    def _inclusive_matrix(self):
        """ Return the inclusive matrix of the temp pivot.

        Returns:
            OpenMaya.MMatrix
        """

        return

    def _add_callbacks(self):
        """

        Returns:
            None
        """
        return

    def _reset_temp_pivot(self):
        """

        Returns:
            None
        """
        if self.pivot:
            cmds.xform(self.pivot, zeroTransformPivots=True)
            self._calculate_relative_matrices()
        return

    def _calculate_relative_matrices(self):
        """ Caluclate relative matrices of current transforms.

        Returns:
            None
        """
        self._relative_matrices = list()

        pivot_transform = KTransform.from_name(self.pivot)

        try:
            inclusive_matrix = pivot_transform.inclusiveMatrix()

        except RuntimeError:
            self._calculate()
            return

        for transform in self.transforms:
            transform_obj = KTransform(transform)
            world_matrix = transform_obj.world_matrix()
            self._relative_matrices.append((transform_obj, world_matrix * inclusive_matrix))

        return

    def _calculate(self):
        if self.pivot:
            rotatePivot = cmds.xform(self.temp_pivot_xform.fullName(), query=True, rotatePivot=True)

            TempPivot.CACHE[self.node.fullName()] = (self._rotate_pivot(), self.o___1____l____0__O____0____l__O)
        try:
            cmds.delete(self.o_____0___O__0_____o_____l_1__0_l____o_____O____0_____O.fullName())
        except:
            pass

        self.calculate_logic3()
        # self.tempPivot_action.setChecked(False)

        cmds.timeControl(mel.eval('$gPlayBackSlider'), edit=True, mainListConnection='animationList')

        # Scene Editor
        # cmds.sceneEditor(unlockMainConnection=True)
        # o_o__o____O_l_o_____o_o__O__o___0___0.unlockMainConnection()

        if self.o__l__O_0___1__o__O_O:
            mel.eval(
                'toggleAutoLoad %sOutlineEd true;' %
                o____0____1_____0_o_0___1__O____1_1.o____1_____1__O_____o____l_O_o___l__O__l___l())

        cmds.setToolTo('moveSuperContext')
        cmds.select([node.fullName() for node in self.transforms or [] if node.fullName() != ''])
        return

    # Public Methods
    def clear(self):
        """ Clear the current temporary pivot properties and delete the cache.

        Returns:
            None
        """
        self.transforms = list()
        self.pivot = str()
        self.clear_cache()
        return

    def add_transform(self, transform):
        """ Append a transform to manipulate.

        Args:
            transform (str): name of the transform object.
        
        Returns:
            None
        """
        if transform not in self.transforms:
            self.transforms.append(transform)
        return

    def pivot_to_last(self):
        """
        
        Returns:
            None
        """
        return

    def pivot_to_center(self):
        """
        
        Returns:
            None
        """
        return


if __name__ == "__main__":
    pass
