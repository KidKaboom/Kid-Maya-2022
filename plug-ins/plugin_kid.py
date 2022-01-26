# :coding: utf-8

# Project Modules
from kid.core.kglobals import MAYA_WINDOW_NAME
from kidui import Toolbar

# Python Modules
import os
import sys
from functools import partial

# Maya Modules
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


class KidCmd(OpenMayaMPx.MPxCommand):
    PLUGIN_PATH = str()
    NAME = "kid"

    MENU_NAME = "kidMenu"
    MENU_LABEL = "Kid"

    @staticmethod
    def creator():
        return OpenMayaMPx.asMPxPtr(KidCmd())

    @staticmethod
    def new_syntax():
        syntax = OpenMaya.MSyntax()
        return syntax

    @staticmethod
    def create_ui():
        KidCmd.delete_ui()

        cmds.menu(KidCmd.MENU_NAME, label=KidCmd.MENU_LABEL, parent=MAYA_WINDOW_NAME, tearOff=True)
        cmds.menuItem(label="Toolbar", command=Toolbar.show)

        return

    @staticmethod
    def delete_ui():
        # Delete Menu
        if cmds.menu(KidCmd.MENU_NAME, exists=True):
            cmds.deleteUI(KidCmd.MENU_NAME, menu=True)

        # Delete Toolbar
        control = Toolbar.NAME + "WorkspaceControl"
        if cmds.control(control, exists=True):
            cmds.deleteUI(control, control=True)

        del Toolbar._instance
        Toolbar._instance = None
        return

    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "Justin Tirado", "1.0.0", "Any")

    try:
        plugin.registerCommand(KidCmd.NAME, KidCmd.creator, KidCmd.new_syntax)
        plugin.registerUI(KidCmd.create_ui, KidCmd.delete_ui)
        KidCmd.PLUGIN_PATH = os.path.split(plugin.loadPath())[0]
    except Exception:
        sys.stderr.write("Failed to register command {} \n".format(KidCmd.NAME))
        raise
    return


def uninitializePlugin(mobject):
    plugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        plugin.deregisterCommand(KidCmd.NAME)
    except Exception:
        sys.stderr.write("Failed to unregister command {}\n".format(KidCmd.NAME))
        raise
    return
