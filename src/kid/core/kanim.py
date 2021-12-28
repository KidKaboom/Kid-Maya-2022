# :coding: utf-8

# Project Modules
from kid.core.kobject import KObject
from kid.core.kanimcurve import KAnimCurve
from kid.core.kkeyframe import KKeyTangent, KKeyFrame

# Python Modules

# Maya Modules
import maya.cmds as cmds


class KAnim(KObject):
    """
    References:
        * http://blog.christianlb.io/creating-an-animation-exporter-with-the-maya-api
    """
    @staticmethod
    def get_keyable(transform):
        """ Returns a list of keyable attribute names from transform name.

        Args:
            transform(str)

        Returns:
            list(str)
        """
        result = list()

        channelbox_selection = cmds.channelBox('mainChannelBox', query=True, selectedMainAttributes=True)

        if channelbox_selection:
            result = channelbox_selection
        else:
            result = cmds.listAttr(transform, keyable=True)

        # Exceptions
        for x in ['translate', 'rotate', 'scale']:
            if x in result:
                result.remove(x)

        return result

    def __init__(self):
        self._anim_curves = list()


if __name__ == '__main__':
    pass
