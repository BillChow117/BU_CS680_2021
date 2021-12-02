"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA2
due date:                   Oct.12,2021

Limb class: Draw a limb without hand or foot, used in ModelArm and ModelLeg, rotation limitation of joints are configured
"""

from wx.core import UpdateUIEvent
from Component import Component
from ModelFinger import ModelFinger
from Point import Point
import ColorType as CT
from DisplayableCube import DisplayableCube
from DisplayableRoundCylinder import DisplayableRoundCylinder
from DisplayableJoint import DisplayableJoint


class ModelLimb(Component):
    components = None
    contextParent = None

    def __init__(self, parent, position, edge = 1, lenth = 3, scale = None, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        self.edge = edge
        self.lenth = lenth
        self.joint_radius = 0.9 * edge/2
        self.joint_length = self.joint_radius * 2

        joint_1 = Component(Point((0,0,0)),DisplayableJoint(self.contextParent,self.joint_radius,self.joint_length))
        joint_1.setDefaultColor(CT.ORANGE)
        self.addChild(joint_1)
        self.components.append(joint_1)

        upper_part = Component(Point((0,0,self.joint_length)),DisplayableCube(self.contextParent,edge,(1,1,lenth)))
        upper_part.setDefaultColor(CT.ORANGE)
        joint_1.addChild(upper_part)
        self.components.append(upper_part)

        joint_2 = Component(Point((0,0,lenth)),DisplayableJoint(self.contextParent,self.joint_radius,self.joint_length))
        joint_2.setDefaultColor(CT.ORANGE)
        upper_part.addChild(joint_2)
        self.components.append(joint_2)

        joint_2.setRotateExtent(joint_2.uAxis,-75,0)
        joint_2.setRotateExtent(joint_2.vAxis,0,0)
        joint_2.setRotateExtent(joint_2.wAxis,0,0)

        lower_part = Component(Point((0,0,self.joint_length)),DisplayableCube(self.contextParent,edge,(1,1,lenth)))
        lower_part.setDefaultColor(CT.ORANGE)
        joint_2.addChild(lower_part)
        self.components.append(lower_part)

        lower_part.setRotateExtent(joint_2.uAxis,-75,0)
        lower_part.setRotateExtent(joint_2.vAxis,0,0)
        lower_part.setRotateExtent(joint_2.wAxis,0,0)

        if scale != None:
                self.setDefaultScale(scale)
        
    def getLastCompLenth(self):
        return self.lenth

    def addChildtoEnd(self,child):
        self.components[-1].addChild(child)
