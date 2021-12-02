"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA2
due date:                   Oct.12,2021

Hand class: Draw a right or left hand, rotation limitation of joints are configured
"""

from Component import Component
from ModelFinger import ModelFinger
from Point import Point
import ColorType as CT
from DisplayableCube import DisplayableCube
from DisplayableJoint import DisplayableJoint


class ModelHand(Component):
    components = None
    contextParent = None

    def __init__(self, parent, position, right_left: bool = True, scale = None, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        wrist_radius = 0.12
        wrist_length = wrist_radius * 2
        wrist = Component(Point((0,0,0)),DisplayableJoint(self.contextParent,wrist_radius,wrist_length))
        wrist.setDefaultColor(CT.ORANGE)
        self.addChild(wrist)
        self.components.append(wrist)
        self.wrist = wrist

        palm_length = 1
        palm_width = 1
        palm_thickness = 2.2 * wrist_radius
        palm_scale = (palm_length, palm_thickness, palm_width)
        palm = Component(Point((0,0,wrist_length)),DisplayableCube(self.contextParent,palm_length,palm_scale))
        palm.setDefaultColor(CT.SEAGREEN)
        wrist.addChild(palm)
        self.components.append(palm)
        self.palm = palm

        finger_radius = palm_thickness/2
        finger_lenth = 1.5*palm_thickness

        # right hand
        if right_left:
            wrist.setRotateExtent(wrist.uAxis,-45,15)
            wrist.setRotateExtent(wrist.vAxis, -5,15)
            wrist.setRotateExtent(wrist.wAxis,-90,45)

            palm.setRotateExtent(wrist.uAxis,-45,15)
            palm.setRotateExtent(wrist.vAxis, -5,15)
            palm.setRotateExtent(wrist.wAxis,0,0)
            
            thumb_finger = ModelFinger(self.contextParent,Point((-palm_length/2,0,palm_length/4)),finger_radius,finger_lenth,2)
            thumb_finger.setDefaultAngle(-45,thumb_finger.vAxis)
            palm.addChild(thumb_finger)
            self.components += thumb_finger.components
            

            Index_finger = ModelFinger(self.contextParent,Point((-palm_length/2 + finger_radius,0,palm_length)),finger_radius,0.9*finger_lenth,3)
            palm.addChild(Index_finger)
            self.components += Index_finger.components
            

            middle_finger = ModelFinger(self.contextParent,Point((finger_radius/3 - palm_length/6,0,palm_length)),finger_radius,finger_lenth,3)
            palm.addChild(middle_finger)
            self.components += middle_finger.components
            

            ring_finger = ModelFinger(self.contextParent,Point((palm_length/6 - finger_radius/3,0,palm_length)),finger_radius,0.9*finger_lenth,3)
            palm.addChild(ring_finger)
            self.components += ring_finger.components
            

            little_finger = ModelFinger(self.contextParent,Point((palm_length/2 - finger_radius,0,palm_length)),finger_radius,0.8*finger_lenth,3)
            palm.addChild(little_finger)
            self.components += little_finger.components
            

            #thumb finger rotation limit
            thumb_finger.setRotateExtent(0,0,-90,0)
            thumb_finger.setRotateExtent(0,1,-30,30)
            thumb_finger.setRotateExtent(0,2,0,0)

            thumb_finger.setRotateExtent(1,0,0,0)
            thumb_finger.setRotateExtent(1,1,0,90)
            thumb_finger.setRotateExtent(1,2,0,0)

        
        #left hand
        else:
            wrist.setRotateExtent(wrist.uAxis,-45,15)
            wrist.setRotateExtent(wrist.vAxis, -15,5)
            wrist.setRotateExtent(wrist.wAxis,-45,90)

            palm.setRotateExtent(wrist.uAxis,-45,15)
            palm.setRotateExtent(wrist.vAxis, -15,5)
            palm.setRotateExtent(wrist.wAxis,0,0)

            thumb_finger = ModelFinger(self.contextParent,Point((palm_length/2,0,palm_length/4)),finger_radius,finger_lenth,2)
            thumb_finger.setDefaultAngle(45,thumb_finger.vAxis)
            palm.addChild(thumb_finger)
            self.components += thumb_finger.components

            Index_finger = ModelFinger(self.contextParent,Point((palm_length/2 - finger_radius,0,palm_length)),finger_radius,0.9*finger_lenth,3)
            palm.addChild(Index_finger)
            self.components += Index_finger.components

            middle_finger = ModelFinger(self.contextParent,Point((palm_length/6 - finger_radius/3,0,palm_length)),finger_radius,finger_lenth,3)
            palm.addChild(middle_finger)
            self.components += middle_finger.components

            ring_finger = ModelFinger(self.contextParent,Point((finger_radius/3 - palm_length/6,0,palm_length)),finger_radius,0.9*finger_lenth,3)
            palm.addChild(ring_finger)
            self.components += ring_finger.components

            little_finger = ModelFinger(self.contextParent,Point((-palm_length/2 + finger_radius,0,palm_length)),finger_radius,0.8*finger_lenth,3)
            palm.addChild(little_finger)
            self.components += little_finger.components

            #thumb finger rotation limit
            thumb_finger.setRotateExtent(0,0,-90,0)
            thumb_finger.setRotateExtent(0,1,-30,30)
            thumb_finger.setRotateExtent(0,2,0,0)

            thumb_finger.setRotateExtent(1,0,0,0)
            thumb_finger.setRotateExtent(1,1,-90,0)
            thumb_finger.setRotateExtent(1,2,0,0)

        self.thumb_finger = thumb_finger
        self.Index_finger = Index_finger
        self.middle_finger = middle_finger
        self.ring_finger = ring_finger
        self.little_finger =little_finger

        #index finger rotation limit
        Index_finger.setRotateExtent(0,0,-90,0)
        Index_finger.setRotateExtent(0,1,-5,5)
        Index_finger.setRotateExtent(0,2,0,0)

        Index_finger.setRotateExtent(1,0,-90,0)
        Index_finger.setRotateExtent(1,1,0,0)
        Index_finger.setRotateExtent(1,2,0,0)

        Index_finger.setRotateExtent(2,0,-90,0)
        Index_finger.setRotateExtent(2,1,0,0)
        Index_finger.setRotateExtent(2,2,0,0)

        #middle finger rotation limit
        middle_finger.setRotateExtent(0,0,-90,0)
        middle_finger.setRotateExtent(0,1,-5,5)
        middle_finger.setRotateExtent(0,2,0,0)

        middle_finger.setRotateExtent(1,0,-90,0)
        middle_finger.setRotateExtent(1,1,0,0)
        middle_finger.setRotateExtent(1,2,0,0)

        middle_finger.setRotateExtent(2,0,-90,0)
        middle_finger.setRotateExtent(2,1,0,0)
        middle_finger.setRotateExtent(2,2,0,0)

        #ring finger rotation limit
        ring_finger.setRotateExtent(0,0,-90,0)
        ring_finger.setRotateExtent(0,1,-5,5)
        ring_finger.setRotateExtent(0,2,0,0)

        ring_finger.setRotateExtent(1,0,-90,0)
        ring_finger.setRotateExtent(1,1,0,0)
        ring_finger.setRotateExtent(1,2,0,0)

        ring_finger.setRotateExtent(2,0,-90,0)
        ring_finger.setRotateExtent(2,1,0,0)
        ring_finger.setRotateExtent(2,2,0,0)

        #little finger rotation limit
        little_finger.setRotateExtent(0,0,-90,0)
        little_finger.setRotateExtent(0,1,-5,5)
        little_finger.setRotateExtent(0,2,0,0)

        little_finger.setRotateExtent(1,0,-90,0)
        little_finger.setRotateExtent(1,1,0,0)
        little_finger.setRotateExtent(1,2,0,0)

        little_finger.setRotateExtent(2,0,-90,0)
        little_finger.setRotateExtent(2,1,0,0)
        little_finger.setRotateExtent(2,2,0,0)

        if scale != None:
            self.setDefaultScale(scale)




