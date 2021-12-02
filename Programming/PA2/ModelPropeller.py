"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA2
due date:                   Oct.12,2021

Propeller class: Draw a small rocket propeller
"""

from wx.core import UpdateUIEvent
from Component import Component
from ModelFinger import ModelFinger
from Point import Point
import ColorType as CT
from DisplayableCube import DisplayableCube
from DisplayableRoundCylinder import DisplayableRoundCylinder
from DisplayableCylinder import DisplayableCylinder
from DisplayableJoint import DisplayableJoint


class ModelPropeller(Component):
    components = None
    contextParent = None

    def __init__(self, parent, position, scale = None, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        self.rocket_lenth = 2
        self.rocket_top_radius = self.rocket_lenth / 4
        self.rocket_bot_radius = self.rocket_lenth * 2 / 3
        self.joint_radius = self.rocket_top_radius
        self.joint_length = self.rocket_top_radius * 2

        joint = Component(Point((0,0,0)),DisplayableJoint(self.contextParent,self.joint_radius,self.joint_length))
        joint.setDefaultColor(CT.ORANGE)
        self.addChild(joint)
        self.joint = joint
        self.components.append(joint)

        propeller = Component(Point((0,0,self.joint_length)),DisplayableCylinder(self.contextParent,self.rocket_top_radius,self.rocket_bot_radius,self.rocket_lenth))
        propeller.setDefaultColor(CT.SILVER)
        propeller.setRotateExtent(propeller.uAxis,0,0)
        propeller.setRotateExtent(propeller.vAxis,0,0)
        propeller.setRotateExtent(propeller.wAxis,0,0)
        joint.addChild(propeller)
        self.propeller = propeller
        self.components.append(propeller)


        if scale != None:
                self.setDefaultScale(scale)
        
 
