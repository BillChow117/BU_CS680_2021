"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA2
due date:                   Oct.12,2021

Finger class: Draw a finger with a configurable number of knuckles, rotation limitation of joints are configured
"""

from Component import Component
from Point import Point
import ColorType as CT
from DisplayableCube import DisplayableCube
from DisplayableRoundCylinder import DisplayableRoundCylinder


class ModelFinger(Component):
    components = None
    contextParent = None

    def __init__(self, parent, position, fingerRadius = 0.05, fingerHeight = 0.15, fingerNumber = 3, scale = None, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        finger0 = Component(Point((0,0,0)),DisplayableRoundCylinder(self.contextParent,fingerRadius,fingerRadius,fingerHeight))
        finger0.setDefaultColor(CT.ORANGE)
        self.addChild(finger0)
        self.components.append(finger0)

        if fingerNumber > 1:
            parent_finger = finger0
            for i in range(fingerNumber - 1):
                curr_finger = Component(Point((0,0,fingerHeight)),DisplayableRoundCylinder(self.contextParent,fingerRadius,fingerRadius,fingerHeight))
                curr_finger.setDefaultColor(CT.ORANGE)
                parent_finger.addChild(curr_finger)
                self.components.append(curr_finger)
                parent_finger = curr_finger

        if scale != None:
            self.setDefaultScale(scale)

    def setRotateExtent(self,index,axis,minDeg=None,maxDeg=None):
        curr_comp = self.components[index]
        if axis == 0:
            curr_comp.setRotateExtent(curr_comp.uAxis,minDeg,maxDeg)
        elif axis == 1:
            curr_comp.setRotateExtent(curr_comp.vAxis,minDeg,maxDeg)
        elif axis == 2:
            curr_comp.setRotateExtent(curr_comp.wAxis,minDeg,maxDeg)
        else:
            raise TypeError("unknown axis for rotation extent setting")

