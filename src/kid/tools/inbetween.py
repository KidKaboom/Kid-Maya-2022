# :coding: utf-8

# Project Modules
from kid.core import KObject, KTransform, KKeyFrame, KMath, KDebug, KAnim

# Python Modules

# Maya Modules
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim


class Inbetween(KObject):
    """ Class that handles creating a keyframe from comparing the previous values with the next values.
    
    References:
        * https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_cpp_ref_anim_export_util_2anim_export_util_8cpp_example_html

    """
    DEFAULT_FAVOR_VALUES = [0.0, .0833, .1666, .2499, .3332, .4165, .5, .5833, .6666, .7499, .8332, .9165, 1.0]
    DEFAULT_OVERSHOOT_VALUES = [-2.0, -1.75, -1.5, -1.25, -1.0, -0.75, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]

    # Static Methods
    @staticmethod
    def favor(transform, attribute, weight):
        """ Sets the keyframe value to favor the previous or next keyframe based on weight.

        Args:
            transform(str)
            attribute(str)
            weight(float)

        Returns:
            None
        """
        query = "{}.{}".format(transform, attribute)
        next_time = cmds.findKeyframe(query, which="next")
        next_value = cmds.getAttr(query, time=next_time)

        previous_time = cmds.findKeyframe(query, which="previous")
        previous_value = cmds.getAttr(query, time=previous_time)
        new_value = (next_value - previous_value) * weight + previous_value

        try:
            pass
            # cmds.setAttr(query, new_value)

        except RuntimeError:
            KDebug.error("""Inbetween: Unable to set "{}".""".format(query))

        return

    @staticmethod
    def favor_all(transform, weight):
        for attribute in KAnim.get_keyable(transform):
            Inbetween.favor(transform, attribute, weight)
        return

    @staticmethod
    def favor_api(transform, attribute, weight):
        return

    # Object Methods
    def __init__(self, transform):
        self._transform = transform

    def is_valid(self):
        if self._transform:
            return True
        return False

    def set_transform(self, transform):
        """ Sets the current transform.

        Args:
            transform(str)

        Returns:
            None
        """
        if not isinstance(transform, str):
            raise TypeError

        self._transform = transform
        return


if __name__ == '__main__':
    transform = "pCube1"

    # # Cmds Version
    # KDebug.update_time()
    # Inbetween.favor_all(transform, .5) # 0.007997989654541016 seconds
    # KDebug.log_elapsed_time()

    # Api Version
    KDebug.update_time()
    
    # Get Dag
    selection = OpenMaya.MSelectionList()
    selection.add(transform)
    dag = OpenMaya.MDagPath()
    selection.getDagPath(0, dag)
    fn = OpenMaya.MFnDependencyNode(dag.node())
    
    # Get Current Time
    current_time = OpenMayaAnim.MAnimControl.currentTime()
    
    # Get Animated Plugs
    plugs = OpenMaya.MPlugArray()
    OpenMayaAnim.MAnimUtil.findAnimatedPlugs(dag, plugs)
    
    for plug_index in range(plugs.length()):
        plug = plugs[plug_index]
        animation = OpenMaya.MObjectArray()
        
        OpenMayaAnim.MAnimUtil.findAnimation(plug, animation)
        
        for anim_index in range(animation.length()):
            anim_object = animation[anim_index]
            
            if not anim_object.hasFn(OpenMaya.MFn.kAnimCurve):
                continue
                
            anim_curve = OpenMayaAnim.MFnAnimCurve(anim_object)
            
            if anim_curve.numKeys() == 0:
                continue
            
            # Get Closet Keyframe
            close_index = anim_curve.findClosest(current_time)
            close_time = anim_curve.time(close_index)
            
            previous_index = None
            next_index = None
            
            if current_time == close_time:
                # Previous Index
                if close_index > 0:
                    previous_index = close_index - 1
                else:
                    previous_index = close_index
                
                # Next Index
                if close_index < anim_curve.numKeys() - 1:
                    next_index = close_index + 1
                else:
                    next_index = close_index
                    
            else:
                # Still not found
                # Previous Index
                if close_index == 0 and current_time < close_time:
                    previous_index = None
                    next_index = 0
                
                # Next Index
                elif close_index == anim_curve.numKeys() - 1 and current_time > close_time:
                    next_index = None
                    previous_index = anim_curve.numKeys() - 1
                
                else:
                    # Search Previous 2 vs Next 2
                    if previous_index is None and next_index is None:
                        distance_query = list()
                        
                        for index in range(close_index - 2, close_index + 3):
                            if 0 <= index <= anim_curve.numKeys() - 1:
                                distance_query.append(abs(current_time.value() - anim_curve.time(index).value()))
                        
                        # Find Min & Max distances
                        distance_min, distance_max = sorted(distance_query)[:2]
                        
                        previous_index = distance_query.index(distance_min)
                        next_index = distance_query.index(distance_max)
                        
                        if previous_index == next_index:
                            next_index += 1
                            
                        elif previous_index > next_index:
                            previous_index -=1
                            next_index += 1
                        
            if previous_index == next_index:
                continue
            
            elif previous_index is None:
                continue
                
            elif next_index is None:
                continue
            
            weight = 0.5
            previous_value = anim_curve.value(previous_index)
            next_value = anim_curve.value(next_index)
            new_value = (next_value - previous_value) * weight + previous_value
            #anim_curve.addKey(current_time, new_value, change=anim_cache)
            anim_curve.addKey(current_time, new_value)
            
            # print(previous_index, next_index)
            
    
    KDebug.log_elapsed_time()
