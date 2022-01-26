# :coding: utf-8

# Project Modules
from kid.__version__ import VERSION
from kid.core import KObject, KDebug
from kidmaya.ui.dock import Dock, MayaQWidgetDockableMixin
from kidmaya.ui.toolbar_widget import ToolbarWidget
from kidqt.__qt__ import *
from kidmaya.tools.command_test import CommandTest


# Python Modules


class Toolbar(Dock):
    """ Class that handles creating building a Maya dock that hosts tools.
    """
    _instance = None
    NAME = "KidToolbar"
    TITLE = "Kid Toolbar " + VERSION

    @staticmethod
    def instance():
        """ Returns the current instance. If None, create a new instance.

        Returns:
            Toolbar
        """
        if Toolbar._instance is None:
            Toolbar()

        return Toolbar._instance

    # @staticmethod
    # def show(*args, **kwargs):
    #     return Dock.show(Toolbar.instance(), dockable=True, debug=True)

    def __init__(self, *args, **kwargs):
        Dock.__init__(self, parent=None, name=Toolbar.NAME, title=Toolbar.TITLE)

        # if Toolbar._instance:
        #     raise Exception("This class is a singleton. Use Toolbar.instance() instead.")

        # Build UI
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        layout.addWidget(ToolbarWidget())

        # Toolbar._instance = self


if __name__ == '__main__':
    # _toolbar = Toolbar.instance()
    # _toolbar.show(dockable=True, debug=True)
    # try:
    #     cmds.deleteUI("KidToolbarWorkspaceControl", control=True)
    # except:
    #     pass
    # Toolbar.show()
    # _test = ToolbarWidget()
    # _test.show(dockable=True)
    _test = Toolbar()
    _test.show(dockable=True, debug=True)
