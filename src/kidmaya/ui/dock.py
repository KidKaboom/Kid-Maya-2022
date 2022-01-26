# :coding: utf-8

# Project Modules
from kidqt.__qt__ import QWidget

# Python Modules
import inspect
from functools import partial

# Maya Modules
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class Dock(MayaQWidgetDockableMixin, QWidget):
    """ Class that handles Dockable UIs in Maya
    
    Args:
        parent(object, None):   Parent object.
        name(str):              Unique object name.
        title(str):             Window title.
        
    """

    @classmethod
    def restore(cls, parent, name, title=str()):
        """ Internal method to restore the UI when Maya is opened.
        
        Args:
            parent(object, None)
            name(str)
            title(str)
        """
        instance = cls(parent, name, title)
        workspace_control = OpenMayaUI.MQtUtil.getCurrentParent()
        mixin_ptr = OpenMayaUI.MQtUtil.findControl(instance.objectName())
        OpenMayaUI.MQtUtil.addWidgetToMayaLayout(mixin_ptr, int(workspace_control))
        return

    def __init__(self, parent, name, title=str()):
        MayaQWidgetDockableMixin.__init__(self, parent)

        # Properties
        self.debug = False

        # Defaults
        self.setObjectName(name)

        if not title:
            title = name

        self.setWindowTitle(title)

        pass

    def show(self, *args, **kwargs):
        control_name = self.objectName() + "WorkspaceControl"

        # Delete Existing
        if "debug" in kwargs:
            if kwargs.get("debug", False):
                if cmds.workspaceControl(control_name, exists=True):
                    try:
                        cmds.deleteUI(control_name, control=True)
                    except RuntimeError:
                        pass
        else:
            if cmds.workspaceControl(control_name, exists=True):
                cmds.workspaceControl(control_name, edit=True, restore=True)
                return

        # Restore UI
        module = inspect.getmodule(self).__name__
        class_name = self.__class__.__name__
        kwargs["uiScript"] = "import {0}; {0}.{1}.restore({2}, {3}, {4})".format(
            module,
            class_name,
            self.parent(),
            self.objectName(),
            self.windowTitle()
            )

        return MayaQWidgetDockableMixin.show(self, *args, **kwargs)


if __name__ == '__main__':
    _dock = Dock(None, "testDock")
    _dock.show(dockable=True, debug=True)
