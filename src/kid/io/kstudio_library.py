# :coding: utf-8

# Project Modules
from kid.core import KObject
from kid.io.kio import KIO
from kid.io.kjson import Kjson

# Python Modules
import getpass

# Maya Modules
import maya.cmds as cmds


class KSLData(KObject):
    def __str__(self):
        return self.str_formatter(**self.as_dict())


class KSLReference(KSLData):
    def __init__(self):
        self.node = str()
        self.unresolved = str()
        self.namespace = str()
        self.filename = str()


class KSLPoseMetadata(KSLData):
    def __init__(self):
        self.mayaSceneFile = str()
        self.angularUnit = str()
        self.description = str()
        self.endFrame = None
        self.linearUnit = str()
        self.version = "1.0.0"
        self.references = list()
        self.user = getpass.getuser()
        self.startFrame = None
        self.timeUnit = str()
        self.mayaVersion = cmds.about(version=True)
        self.ctime = str()


class KSLMirrorMetadata(KSLData):
    def __init__(self):
        self.mirrorPlane = [-1, 1, 1]
        self.right = "_R"
        self.left = "_L"
        self.description = str()
        self.mayaVersion = cmds.about(version=True)
        self.version = "1.0.0"
        self.references = list()
        self.user = getpass.getuser()
        self.mayaSceneFile = str()
        self.ctime = str()


class KSLAttribute(KSLData):
    def __init__(self):
        self.curve = str()
        self.type = str()
        self.value = None


class KSLMirrorAttribute(KSLData):
    def __init__(self):
        self.mirrorAxis = [-1, 1, 1]


class KSLObject(KSLData):
    def __init__(self):
        self.attrs = list()


class KSLPose(KIO):
    """ Class that handles Studio Library reading and writitng .pose files.

    Hierarchy:
        * .pose (directory)
            * pose.json
            * thumbnail.jpg
    """

    def extension(self):
        return ".pose"

    def write_handler(self, *args, **kwargs):
        pass

    def read_handler(self, *args, **kwargs):
        pass


class KSLSet(KIO):
    """ Class that handles Studio Library reading and writitng .set files.

    Hierarchy:
        * .set (directory)
            * set.json
            * thumbnail.jpg
    """

    def extension(self):
        return ".set"

    def write_handler(self, *args, **kwargs):
        pass

    def read_handler(self, *args, **kwargs):
        pass


class KSLMirror(KIO):
    """ Class that handles Studio Library reading and writitng .mirror files.

    Hierarchy:
        * .mirror (directory)
            * mirrortable.json
            * thumbnail.jpg
    """

    def extension(self):
        return ".mirror"

    def write_handler(self, *args, **kwargs):
        pass

    def read_handler(self, *args, **kwargs):
        pass


class KSLAnim(KIO):
    """ Class that handles Studio Library reading and writitng .anim files.

    Hierarchy:
        * .anim (directory)
            * sequence (directory)
                * thumbnail.####.jpg
            * animationa.ma
            * pose.json
            * thumbnail.0000.jpg
            * thumbnail.jpg
    """

    def extension(self):
        return ".anim"

    def write_handler(self, *args, **kwargs):
        pass

    def read_handler(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    _test_path = "D:\\Jobs\\Treyarch\\Resource\\Soldier\\Soldier_Default.pose\\pose.json"
