"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA2
due date:                   Oct.12,2021

Leg class: Draw a right or left leg, rotation limitation of joints are configured
"""

from Component import Component
from Point import Point
import ColorType as CT
from DisplayableJoint import DisplayableJoint
from DisplayableTrapezoid import DisplayableTrapezoid
from ModelLimb import ModelLimb


class ModelLeg(Component):
    components = None
    contextParent = None

    def __init__(self, parent, position, right_left: bool = True, edge = 1.2, lenth = 3.6, scale = None, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        limb = ModelLimb(self.contextParent,Point((0,0,0)),edge,lenth)
        self.addChild(limb)
        self.components += limb.components
        self.limb = limb

        limb.components[2].setRotateExtent(limb.components[2].uAxis,0,75)
        limb.components[3].setRotateExtent(limb.components[3].uAxis,0,75)
        
        len = limb.getLastCompLenth()
        ankle_radius = 0.9 * edge/2
        ankle_lenth = ankle_radius * 2

        ankle = Component(Point((0,0,len)),DisplayableJoint(self.contextParent,ankle_radius,ankle_lenth))
        ankle.setDefaultColor(CT.ORANGE)
        ankle.setRotateExtent(ankle.uAxis,-25,35)
        ankle.setRotateExtent(ankle.vAxis,-15,15)
        ankle.setRotateExtent(ankle.wAxis,-15,15)
        limb.addChildtoEnd(ankle)
        self.components.append(ankle)
        self.ankle = ankle

        foot = Component(Point((0,0,ankle_lenth)),DisplayableTrapezoid(self.contextParent,3 * ankle_radius,2 * ankle_radius,ankle_radius,(0.5,1,1)))
        foot.setDefaultColor(CT.ORANGE)
        foot.setRotateExtent(foot.uAxis,-25,35)
        foot.setRotateExtent(foot.vAxis,-15,15)
        foot.setRotateExtent(foot.wAxis,-15,15)
        ankle.addChild(foot)
        self.components.append(foot)
        self.foot = foot

        # set rotation limit of the hip joint
        if right_left:
            limb.components[0].setRotateExtent(limb.components[0].uAxis,-90,90)
            limb.components[0].setRotateExtent(limb.components[0].vAxis,-90,-45)
            limb.components[0].setRotateExtent(limb.components[0].wAxis,0,0)
            limb.components[0].setDefaultAngle(-45,limb.components[0].vAxis)

            limb.components[1].setRotateExtent(limb.components[1].uAxis,0,0)
            limb.components[1].setRotateExtent(limb.components[1].vAxis,0,50)
            limb.components[1].setRotateExtent(limb.components[1].wAxis,-10,45)
            limb.components[1].setDefaultAngle(45,limb.components[1].vAxis)

        else:
            limb.components[0].setRotateExtent(limb.components[0].uAxis,-90,90)
            limb.components[0].setRotateExtent(limb.components[0].vAxis,45,90)
            limb.components[0].setRotateExtent(limb.components[0].wAxis,0,0)
            limb.components[0].setDefaultAngle(45,limb.components[0].vAxis)

            limb.components[1].setRotateExtent(limb.components[1].uAxis,0,0)
            limb.components[1].setRotateExtent(limb.components[1].vAxis,-50,0)
            limb.components[1].setRotateExtent(limb.components[1].wAxis,-45,10)
            limb.components[1].setDefaultAngle(-45,limb.components[1].vAxis)
            

        if scale != None:
                self.setDefaultScale(scale)
        



