# Python Modules
import os

# Maya Modules
from maya import mel

#
import aToolsMod

from maya import cmds

FILE_PATH = __file__


class BaseSubUI(object):
    def __init__(self, parent, buttonSizeDict):
        self.btnSizeDict = buttonSizeDict
        self.parentLayout = parent

        # get values
        self.ws = self.btnSizeDict["small"][0]
        self.hs = self.btnSizeDict["small"][1]
        self.wb = self.btnSizeDict["big"][0]
        self.hb = self.btnSizeDict["big"][1]


def getImagePath(imageName, ext="png", imageFolder="img"):
    imageFile = "%s.%s" % (imageName, ext)
    relativePath = os.path.abspath(os.path.join(FILE_PATH, os.pardir, os.pardir))
    imgPath = os.path.abspath(os.path.join(relativePath, imageFolder, imageFile))

    return imgPath


def getModulePath(filePath, moduleName):
    relativePath = os.sep.join(filePath.split(os.sep)[:-1])
    return relativePath + os.sep + moduleName


def getModKeyPressed():
    mods = cmds.getModifiers()
    if mods == 1:
        return "shift"
    if mods == 4:
        return "ctrl"
    if mods == 8:
        return "alt"
    if mods == 5:
        return "ctrlShift"
    if mods == 9:
        return "altShift"
    if mods == 12:
        return "altCtrl"
    if mods == 13:
        return "altCtrlShift"


def clearMenuItems(menu):
    menuItens = cmds.popupMenu(menu, query=True, itemArray=True)

    if menuItens:
        for loopMenu in menuItens:
            if cmds.menuItem(loopMenu, query=True, exists=True):
                cmds.deleteUI(loopMenu)


def getNameSpace(objects):
    nameSpaces = []
    objectNames = []
    for loopObj in objects:

        nameSpaceIndex = loopObj.find(":") + 1
        nameSpace = loopObj[:nameSpaceIndex]
        objName = loopObj[nameSpaceIndex:]

        nameSpaces.append(nameSpace)
        objectNames.append(objName)

    return [nameSpaces, objectNames]


def getAnimCurves(forceGetFromGraphEditor=False):
    # get selected anim curves from graph editor
    animCurves = cmds.keyframe(query=True, name=True, selected=True)
    # graphEditorFocus = cmds.getPanel(withFocus=True) == "graphEditor1"
    visiblePanels = cmds.getPanel(visiblePanels=True)
    graphEditor = None
    for loopPanel in visiblePanels:
        if loopPanel == "graphEditor1":
            graphEditor = True
            break
    getFrom = "graphEditor"
    if not animCurves or not graphEditor and not forceGetFromGraphEditor:  # get from timeline
        getFrom = "timeline"
        G.playBackSliderPython = G.playBackSliderPython or mel.eval('$aTools_playBackSliderPython=$gPlayBackSlider')
        animCurves = cmds.timeControl(G.playBackSliderPython, query=True, animCurveNames=True)

    return [animCurves, getFrom]


def getTimelineRange(float=True):
    # if G.lastCurrentFrame == cmds.currentTime(query=True): return G.lastRange

    G.playBackSliderPython = G.playBackSliderPython or mel.eval('$aTools_playBackSliderPython=$gPlayBackSlider')
    range = cmds.timeControl(G.playBackSliderPython, query=True, rangeArray=True)
    if float:
        range[1] -= .0001
    # G.lastRange        = range
    # G.lastCurrentFrame = cmds.currentTime(query=True)

    return range


def getTarget(target, animCurves=None, getFrom=None, rangeAll=None):
    # object from curves, object selected, anim curves, attributes, keytimes, keys selected

    if target == "keysSel" or target == "keysIndexSel":
        if animCurves:
            keysSel = []
            if getFrom == "graphEditor":
                for node in animCurves:
                    if target == "keysSel":
                        keysSel.append(cmds.keyframe(node, selected=True, query=True, timeChange=True))
                    if target == "keysIndexSel":
                        keysSel.append(cmds.keyframe(node, selected=True, query=True, indexValue=True))
            else:
                if rangeAll is None:
                    range = getTimelineRange()

                allKeys = [cmds.keyframe(node, query=True, timeChange=True) for node in animCurves if
                           cmds.objExists(node)]
                allIndexKeys = [cmds.keyframe(node, query=True, indexValue=True) for node in animCurves if
                                cmds.objExists(node)]
                keysSel = []
                for n, loopKeyArrays in enumerate(allKeys):
                    keysSel.append([])
                    if loopKeyArrays:
                        for nn, loopKey in enumerate(loopKeyArrays):

                            if rangeAll or range[0] <= loopKey < range[1]:
                                if target == "keysSel":
                                    keysSel[n].append(loopKey)
                                if target == "keysIndexSel":
                                    keysSel[n].append(allIndexKeys[n][nn])

            return keysSel


def createNull(locatorName="tmp"):
    with G.aToolsBar.createAToolsNode: newNull = cmds.spaceLocator(name=locatorName)[0]

    cmds.xform(cp=True)
    cmds.setAttr(".localScaleX", 0)
    cmds.setAttr(".localScaleY", 0)
    cmds.setAttr(".localScaleZ", 0)

    return newNull


def group(nodes=None, name="aTools_group", empty=True, world=False):
    with G.aToolsBar.createAToolsNode:
        if nodes:
            newGroup = cmds.group(nodes, empty=False, name=name, world=world)
        else:
            newGroup = cmds.group(empty=empty, name=name, world=world)
    return newGroup

def saveInfoWithScene(storeNode, attr, value):
    with G.aToolsBar.createAToolsNode:
        cmds.undoInfo(stateWithoutFlush=False)
        currSel = None
        if not cmds.objExists(G.A_NODE) or not cmds.objExists(storeNode):
            currSel = cmds.ls(selection=True)
        if not cmds.objExists(G.A_NODE):
            cmds.createNode('mute', name=G.A_NODE)
        if not cmds.objExists(storeNode):
            cmds.createNode('mute', name=storeNode)
        if currSel:
            cmds.select(currSel)

        if not cmds.isConnected("%s.output" % G.A_NODE, "%s.mute" % storeNode):
            cmds.connectAttr("%s.output" % G.A_NODE, "%s.mute" % storeNode)
        if not cmds.objExists("%s.%s" % (storeNode, attr)):
            cmds.addAttr(storeNode, longName=attr, dataType="string", keyable=False)
        cmds.setAttr("%s.%s" % (storeNode, attr), value, type="string")
        cmds.undoInfo(stateWithoutFlush=True)


def loadInfoWithScene(storeNode, attr):
    obj = "%s.%s" % (storeNode, attr)
    if cmds.objExists(obj):
        return cmds.getAttr(obj)
    else:
        return None


class TempCustomPivot(object):

    def __init__(self):
        self.STORE_NODE = "tempCustomPivot"
        self.CONSTRAINTS = "constraintObjects"
        self.LOCATORS = "locatorObjects"
        self.CTRLS = "ctrlsObjects"
        self.CURRENTFRAME = "currentFrame"
        self.sel = []
        self.deniedCtx = ["dragAttrContext", "manipMoveContext", "manipRotateContext", "manipScaleContext"]

        self.clear()

    def popupMenu(self, *args):
        cmds.popupMenu()
        cmds.menuItem(label="Clear temporary custom pivots", command=self.clear)

    def create(self, *args):

        img = cmds.iconTextButton("TempCustomPivotBtn", query=True, image=True)
        onOff = (img[-10:-4] == "active")
        if onOff:
            self.clear()
            cmds.select(self.sel)
            return

        cmds.undoInfo(openChunk=True)
        cmds.undoInfo(closeChunk=True)
        cmds.undoInfo(openChunk=True)
        cmds.undoInfo(closeChunk=True)
        cmds.undoInfo(openChunk=True)
        cmds.undoInfo(closeChunk=True)
        cmds.undoInfo(openChunk=True)

        self.clear()

        getCurves = getAnimCurves()
        animCurves = getCurves[0]
        getFrom = getCurves[1]

        if animCurves:
            keyTimes = getTarget("keyTimes", animCurves, getFrom)

        self.sel = cmds.ls(selection=True)
        if not self.sel:
            return

        cmds.iconTextButton("TempCustomPivotBtn", edit=True,
                            image=uiMod.getImagePath("specialTools_create_temp_custom_pivot_active"),
                            highlightImage=uiMod.getImagePath("specialTools_create_temp_custom_pivot_active"))

        targetObj = self.sel[-1]
        aToolsMod.saveInfoWithScene(self.STORE_NODE, self.CTRLS, self.sel)

        currentFrame = cmds.currentTime(query=True)
        aToolsMod.saveInfoWithScene(self.STORE_NODE, self.CURRENTFRAME, currentFrame)

        locators = []
        for loopSel in self.sel:
            nameSpace = getNameSpace([loopSel])
            loopSelName = "%s_%s" % (nameSpace[0][0], nameSpace[1][0])
            locatorName = "tempCustomPivot_%s" % loopSelName

            locator = createNull(locatorName)
            locators.append(locator)

            G.aToolsBar.align.align([locator], loopSel)

        locatorGroup = "tempCustomPivot_group"
        group(name=locatorGroup)
        G.aToolsBar.align.align([locatorGroup], targetObj)
        with G.aToolsBar.createAToolsNode:
            cmds.parent(locators, locatorGroup)
        cmds.select(locatorGroup, replace=True)

        locators.append(locatorGroup)

        aToolsMod.saveInfoWithScene(self.STORE_NODE, self.LOCATORS, locators)

        # parent ctrls to locator
        constraints = ["%s_tempCustomPivot_constraint" % loopConstraint for loopConstraint in self.sel]

        aToolsMod.saveInfoWithScene(self.STORE_NODE, self.CONSTRAINTS, constraints)

        for n, loopSel in enumerate(self.sel):
            with G.aToolsBar.createAToolsNode:
                cmds.parentConstraint(locators[n], loopSel, name=constraints[n], maintainOffset=True)
            constraintNode = "%s.blendParent1" % loopSel
            if not cmds.objExists(constraintNode):
                continue
            cmds.setKeyframe(constraintNode)
            if keyTimes:
                for loopTime in keyTimes[0]:
                    cmds.setKeyframe("%s.tx" % locatorGroup, time=(loopTime, loopTime))
                    if loopTime != currentFrame:
                        cmds.setKeyframe(constraintNode, time=(loopTime, loopTime), value=0)

        # enter edit mode
        cmds.setToolTo(cmds.currentCtx())
        cmds.ctxEditMode()

        # scriptjob
        cmds.scriptJob(runOnce=True, killWithScene=True, event=('SelectionChanged', self.scriptJob_SelectionChanged))

    def scriptJob_SelectionChanged(self):
        self.clear()
        cmds.undoInfo(closeChunk=True)

    def clear(self, *args):

        if cmds.iconTextButton("TempCustomPivotBtn", query=True, exists=True):
            cmds.iconTextButton("TempCustomPivotBtn", edit=True,
                                image=uiMod.getImagePath("specialTools_create_temp_custom_pivot"),
                                highlightImage=uiMod.getImagePath("specialTools_create_temp_custom_pivot copy"))

        cmds.refresh(suspend=True)

        currFrame = cmds.currentTime(query=True)

        loadConstraints = aToolsMod.loadInfoWithScene(self.STORE_NODE, self.CONSTRAINTS)
        loadLocators = aToolsMod.loadInfoWithScene(self.STORE_NODE, self.LOCATORS)
        loadCtrls = aToolsMod.loadInfoWithScene(self.STORE_NODE, self.CTRLS)
        currentFrame = aToolsMod.loadInfoWithScene(self.STORE_NODE, self.CURRENTFRAME)

        # exit edit mode

        if cmds.currentCtx() not in self.deniedCtx:
            cmds.setToolTo(cmds.currentCtx())

        if currentFrame:
            cmds.currentTime(eval(currentFrame))

        # get values
        """
        rotation = []
        rotation    = []
        if loadCtrls: 
            ctrlObjs    = eval(loadCtrls)
            for loopCtrl in ctrlObjs:
                rotation.append(cmds.xform(loopCtrl, query=True, ws=True, rotatePivot=True))
                rotation.append(cmds.xform(loopCtrl, query=True, ws=True, rotation=True))
        """

        if loadConstraints:
            constraintObjs = eval(loadConstraints)
            for loopConstraint in constraintObjs:
                if cmds.objExists(loopConstraint):
                    cmds.delete(loopConstraint)

        if loadCtrls and loadLocators:
            locatorObjs = eval(loadLocators)
            ctrlObjs = eval(loadCtrls)
            for n, loopCtrl in enumerate(ctrlObjs):
                if cmds.objExists(loopCtrl) and cmds.objExists(locatorObjs[n]):
                    G.aToolsBar.align.align([loopCtrl], locatorObjs[n])

            for loopLocator in locatorObjs:
                if cmds.objExists(loopLocator):
                    cmds.delete(loopLocator)

        cmds.currentTime(currFrame)
        cmds.refresh(suspend=False)
