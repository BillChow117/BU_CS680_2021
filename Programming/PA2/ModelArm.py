"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA2
due date:                   Oct.12,2021

Arm class: Draw a right or left arm, rotation limitation of joints are configured
"""

from wx.core import UpdateUIEvent
from Component import Component
from ModelFinger import ModelFinger
from ModelHand import ModelHand
from Point import Point
import ColorType as CT
from DisplayableCube import DisplayableCube
from DisplayableRoundCylinder import DisplayableRoundCylinder
from DisplayableJoint import DisplayableJoint
from ModelLimb import ModelLimb


class ModelArm(Component):
    components = None
    contextParent = None

    def __init__(self, parent, position, right_left: bool = True, edge = 1, lenth = 3, scale = None, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        limb = ModelLimb(self.contextParent,Point((0,0,0)),edge,lenth)
        self.addChild(limb)
        self.components += limb.components
        self.limb = limb
        
        len = limb.getLastCompLenth()

        hand = ModelHand(self.contextParent,Point((0,0,len)),right_left,scale=(1.1,1.1,1.1))
        limb.addChildtoEnd(hand)
        self.components += hand.components
        self.hand = hand

        #set rotation limit of the shoulder joint
        if right_left:
            
            limb.components[0].setRotateExtent(limb.components[0].uAxis,-180,180)
            limb.components[0].setRotateExtent(limb.components[0].vAxis,-135,-45)
            limb.components[0].setRotateExtent(limb.components[0].wAxis,0,0)
            limb.components[0].setDefaultAngle(-45,limb.components[0].vAxis)

            limb.components[1].setRotateExtent(limb.components[1].uAxis,0,0)
            limb.components[1].setRotateExtent(limb.components[1].vAxis,-45,50)
            limb.components[1].setRotateExtent(limb.components[1].wAxis,-90,90)
            limb.components[1].setDefaultAngle(45,limb.components[1].vAxis)
            limb.components[1].setDefaultAngle(-90,limb.components[1].wAxis)
        else:
            limb.components[0].setRotateExtent(limb.components[0].uAxis,-180,180)
            limb.components[0].setRotateExtent(limb.components[0].vAxis,45,135)
            limb.components[0].setRotateExtent(limb.components[0].wAxis,0,0)
            limb.components[0].setDefaultAngle(45,limb.components[0].vAxis)

            limb.components[1].setRotateExtent(limb.components[1].uAxis,0,0)
            limb.components[1].setRotateExtent(limb.components[1].vAxis,-50,45)
            limb.components[1].setRotateExtent(limb.components[1].wAxis,-90,90)
            limb.components[1].setDefaultAngle(-45,limb.components[1].vAxis)
            limb.components[1].setDefaultAngle(90,limb.components[1].wAxis)

        if scale != None:
                self.setDefaultScale(scale)
        



