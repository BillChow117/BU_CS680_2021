"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA2
due date:                   Oct.12,2021

Head class: Draw a cube head with a neck and two eyes, rotation limitation of joints are configured
"""

from Component import Component
from ModelEye import ModelEye
from ModelFinger import ModelFinger
from Point import Point
import ColorType as CT
from DisplayableCube import DisplayableCube
from DisplayableRoundCylinder import DisplayableRoundCylinder
from DisplayableJoint import DisplayableJoint
from DisplayableSphere import DisplayableSphere
from Quaternion import Quaternion


class ModelHead(Component):
    components = None
    contextParent = None

    def __init__(self, parent, position, scale = None, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        neck_radius = 0.5
        neck_length = neck_radius * 2
        neck = Component(Point((0,0,0)),DisplayableJoint(self.contextParent,neck_radius,neck_length))
        neck.setDefaultColor(CT.ORANGE)
        neck.setRotateExtent(neck.uAxis,-15,45)
        neck.setRotateExtent(neck.vAxis,-15,15)
        neck.setRotateExtent(neck.wAxis,-80,80)
        self.addChild(neck)
        self.components.append(neck)
        self.neck = neck

        head_edge = 2
        head = Component(Point((0,0,neck_length)),DisplayableCube(self.contextParent,head_edge))
        head.setDefaultColor(CT.ORANGE)
        head.setRotateExtent(head.uAxis,-15,45)
        head.setRotateExtent(head.vAxis,-15,15)
        head.setRotateExtent(head.wAxis,0,0)
        neck.addChild(head)
        self.components.append(head)
        self.head = head

        eye_radius = head_edge / 5

        right_eye = ModelEye(self.contextParent,Point((-head_edge/4,-head_edge/2,head_edge*2/3)),eye_radius)
        head.addChild(right_eye)
        self.components += right_eye.components
        self.right_eye = right_eye

        left_eye = ModelEye(self.contextParent,Point((head_edge/4,-head_edge/2,head_edge*2/3),eye_radius))
        head.addChild(left_eye)
        self.components += left_eye.components
        self.left_eye = left_eye

    
        self.setDefaultAngle(180,self.uAxis)


        if scale != None:
            self.setDefaultScale(scale)




