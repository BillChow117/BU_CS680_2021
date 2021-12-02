"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA2
due date:                   Oct.12,2021

Robot class: The complete creature, rotation limitation of joints are configured
"""

from Component import Component
from ModelPropeller import ModelPropeller
from Point import Point
import ColorType as CT
from DisplayableCube import DisplayableCube
from DisplayableTrapezoid import DisplayableTrapezoid
from ModelHead import ModelHead
from ModelArm import ModelArm
from ModelLeg import ModelLeg
 

class ModelRobot(Component):
    components = None
    contextParent = None

    def __init__(self, parent, position, scale = None, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        chest_top_edge = 5
        chest_bot_edge = 3
        chest_len = 3
        chest_scale=(-1,0.3,-1)

        # Build a fixed waist
        waist_edge = 2 * chest_bot_edge
        waist_scale = (0.5,0.3,0.5)
        waist = Component(Point((0,0,0)),DisplayableCube(self.contextParent,waist_edge,waist_scale))
        waist.setDefaultColor(CT.ORANGE)
        waist.setDefaultAngle(90,waist.uAxis)
        waist.setRotateExtent(waist.uAxis,90,90)
        waist.setRotateExtent(waist.vAxis,0,0)
        waist.setRotateExtent(waist.wAxis,0,0)
        self.addChild(waist)
        self.components.append(waist)
        self.waist = waist

        # Build a chest
        chest = Component(Point((0,0,chest_bot_edge/3)),DisplayableTrapezoid(self.contextParent,chest_top_edge,chest_bot_edge,chest_len,chest_scale))
        chest.setDefaultColor(CT.ORANGE)
        chest.setRotateExtent(chest.uAxis,-30,60)
        chest.setRotateExtent(chest.vAxis,-10,10)
        chest.setRotateExtent(chest.wAxis,-45,45)
        waist.addChild(chest)
        self.components.append(chest)
        self.chest = chest

        # Build a head
        head = ModelHead(self.contextParent,Point((0,0,-2*chest_len)))
        chest.addChild(head)
        self.components += head.components
        self.head = head

        # Two rocket prepellers on the back
        right_prepeller = ModelPropeller(self.contextParent,Point((-chest_top_edge/3,-chest_top_edge*chest_scale[1],3/2*chest_len*chest_scale[2])))
        right_prepeller.joint.setDefaultAngle(30,right_prepeller.joint.uAxis)
        right_prepeller.joint.setRotateDirection(1,-1)
        right_prepeller.joint.setRotateDirection(2,-1)
        right_prepeller.joint.setRotateExtent(right_prepeller.joint.uAxis,30,150)
        right_prepeller.joint.setRotateExtent(right_prepeller.joint.vAxis,-90,5)
        right_prepeller.joint.setRotateExtent(right_prepeller.joint.wAxis,0,0)
        chest.addChild(right_prepeller)
        self.right_prepeller = right_prepeller
        self.components += right_prepeller.components

        left_prepeller = ModelPropeller(self.contextParent,Point((chest_top_edge/3,-chest_top_edge*chest_scale[1],3/2*chest_len*chest_scale[2])))
        left_prepeller.joint.setDefaultAngle(30,left_prepeller.joint.uAxis)
        left_prepeller.joint.setRotateExtent(left_prepeller.joint.uAxis,30,150)
        left_prepeller.joint.setRotateExtent(left_prepeller.joint.vAxis,-5,90)
        left_prepeller.joint.setRotateExtent(left_prepeller.joint.wAxis,0,0)
        chest.addChild(left_prepeller)
        self.left_prepeller = left_prepeller
        self.components += left_prepeller.components

        # Build the right arm
        right_arm = ModelArm(self.contextParent,Point((-(chest_top_edge*2/3 + chest_bot_edge/3),0,-2*2/3*chest_len)),True)
        
        # set rotate direction for mirror rotation
        # shoulder joint
        right_arm.components[0].setRotateDirection(1,-1)
        # upper arm
        right_arm.components[1].setRotateDirection(1,-1)
        right_arm.components[1].setRotateDirection(2,-1)
        # wrist
        right_arm.components[4].setRotateDirection(1,-1)
        right_arm.components[4].setRotateDirection(2,-1)
        # palm
        right_arm.components[5].setRotateDirection(1,-1)
        right_arm.components[5].setRotateDirection(2,-1)
        # thumb finger
        right_arm.components[6].setRotateDirection(1,-1)

        chest.addChild(right_arm)
        self.components += right_arm.components
        self.right_arm = right_arm

        # Build the left arm
        left_arm = ModelArm(self.contextParent,Point((chest_top_edge*2/3 + chest_bot_edge/3,0,-2*2/3*chest_len)),False)
        chest.addChild(left_arm)
        self.components += left_arm.components
        self.left_arm = left_arm

        curr_waist_edge_x = waist_edge * waist_scale[0]
        curr_waist_edge_y = waist_edge * waist_scale[1]
        curr_waist_edge_z = waist_edge * waist_scale[2]


        # Build the right leg
        right_leg = ModelLeg(self.contextParent,Point((-curr_waist_edge_x/2,0,curr_waist_edge_z*3/4)),True)
        
        # set rotate direction for mirror rotation
        # hip joint
        right_leg.components[0].setRotateDirection(1,-1)
        # thigh
        right_leg.components[1].setRotateDirection(1,-1)
        right_leg.components[1].setRotateDirection(2,-1)
        # ankle
        right_leg.components[4].setRotateDirection(1,-1)
        right_leg.components[4].setRotateDirection(2,-1)
        # foot
        right_leg.components[5].setRotateDirection(1,-1)
        right_leg.components[5].setRotateDirection(2,-1)

        
        waist.addChild(right_leg)
        self.components += right_leg.components
        self.right_leg = right_leg


        # Build the left leg
        left_leg = ModelLeg(self.contextParent,Point((curr_waist_edge_x/2,0,curr_waist_edge_z*3/4)),False)
        waist.addChild(left_leg)
        self.components += left_leg.components
        self.left_leg =left_leg


        if scale != None:
            self.setDefaultScale(scale)

    def test_case_1(self):
        # Right arm
        self.right_arm.limb.components[1].setCurrentAngle(0,self.right_arm.limb.components[1].vAxis)
        self.right_arm.limb.components[1].setCurrentAngle(90,self.right_arm.limb.components[1].wAxis)
        self.right_arm.limb.components[2].setCurrentAngle(-45,self.right_arm.limb.components[2].uAxis)
        self.right_arm.limb.components[3].setCurrentAngle(-45,self.right_arm.limb.components[3].uAxis)

        # Right hand
        self.right_arm.hand.wrist.setCurrentAngle(-90,self.right_arm.hand.wrist.wAxis)

        self.right_arm.hand.thumb_finger.components[0].setCurrentAngle(-30,self.right_arm.hand.thumb_finger.components[0].vAxis)

        self.right_arm.hand.Index_finger.components[0].setCurrentAngle(-90,self.right_arm.hand.Index_finger.components[0].uAxis)
        self.right_arm.hand.Index_finger.components[1].setCurrentAngle(-90,self.right_arm.hand.Index_finger.components[1].uAxis)
        self.right_arm.hand.Index_finger.components[2].setCurrentAngle(-90,self.right_arm.hand.Index_finger.components[2].uAxis)

        self.right_arm.hand.middle_finger.components[0].setCurrentAngle(-90,self.right_arm.hand.middle_finger.components[0].uAxis)
        self.right_arm.hand.middle_finger.components[1].setCurrentAngle(-90,self.right_arm.hand.middle_finger.components[1].uAxis)
        self.right_arm.hand.middle_finger.components[2].setCurrentAngle(-90,self.right_arm.hand.middle_finger.components[2].uAxis)

        self.right_arm.hand.ring_finger.components[0].setCurrentAngle(-90,self.right_arm.hand.ring_finger.components[0].uAxis)
        self.right_arm.hand.ring_finger.components[1].setCurrentAngle(-90,self.right_arm.hand.ring_finger.components[1].uAxis)
        self.right_arm.hand.ring_finger.components[2].setCurrentAngle(-90,self.right_arm.hand.ring_finger.components[2].uAxis)

        self.right_arm.hand.little_finger.components[0].setCurrentAngle(-90,self.right_arm.hand.little_finger.components[0].uAxis)
        self.right_arm.hand.little_finger.components[1].setCurrentAngle(-90,self.right_arm.hand.little_finger.components[1].uAxis)
        self.right_arm.hand.little_finger.components[2].setCurrentAngle(-90,self.right_arm.hand.little_finger.components[2].uAxis)       

    def test_case_2(self):
        # Right arm
        self.right_arm.limb.components[1].setCurrentAngle(15,self.right_arm.limb.components[1].vAxis)
        self.right_arm.limb.components[1].setCurrentAngle(75,self.right_arm.limb.components[1].wAxis)
        self.right_arm.limb.components[2].setCurrentAngle(-75,self.right_arm.limb.components[2].uAxis)
        self.right_arm.limb.components[3].setCurrentAngle(-75,self.right_arm.limb.components[3].uAxis)

        # Right hand
        self.right_arm.hand.wrist.setCurrentAngle(-90,self.right_arm.hand.wrist.wAxis)

        self.right_arm.hand.thumb_finger.components[0].setCurrentAngle(-90,self.right_arm.hand.thumb_finger.components[0].uAxis)
        self.right_arm.hand.thumb_finger.components[1].setCurrentAngle(90,self.right_arm.hand.thumb_finger.components[1].vAxis)

        self.right_arm.hand.Index_finger.components[0].setCurrentAngle(-5,self.right_arm.hand.Index_finger.components[0].vAxis)

        self.right_arm.hand.middle_finger.components[0].setCurrentAngle(5,self.right_arm.hand.middle_finger.components[0].vAxis)

        self.right_arm.hand.ring_finger.components[0].setCurrentAngle(-90,self.right_arm.hand.ring_finger.components[0].uAxis)
        self.right_arm.hand.ring_finger.components[1].setCurrentAngle(-90,self.right_arm.hand.ring_finger.components[1].uAxis)
        self.right_arm.hand.ring_finger.components[2].setCurrentAngle(-90,self.right_arm.hand.ring_finger.components[2].uAxis)

        self.right_arm.hand.little_finger.components[0].setCurrentAngle(-90,self.right_arm.hand.little_finger.components[0].uAxis)
        self.right_arm.hand.little_finger.components[1].setCurrentAngle(-90,self.right_arm.hand.little_finger.components[1].uAxis)
        self.right_arm.hand.little_finger.components[2].setCurrentAngle(-90,self.right_arm.hand.little_finger.components[2].uAxis)

        
        # Left arm
        self.left_arm.limb.components[1].setCurrentAngle(-15,self.left_arm.limb.components[1].vAxis)
        self.left_arm.limb.components[1].setCurrentAngle(-75,self.left_arm.limb.components[1].wAxis)
        self.left_arm.limb.components[2].setCurrentAngle(-75,self.left_arm.limb.components[2].uAxis)
        self.left_arm.limb.components[3].setCurrentAngle(-75,self.left_arm.limb.components[3].uAxis)

        # Left hand
        self.left_arm.hand.wrist.setCurrentAngle(90,self.left_arm.hand.wrist.wAxis)

        self.left_arm.hand.thumb_finger.components[0].setCurrentAngle(-90,self.left_arm.hand.thumb_finger.components[0].uAxis)
        self.left_arm.hand.thumb_finger.components[1].setCurrentAngle(-90,self.left_arm.hand.thumb_finger.components[1].vAxis)

        self.left_arm.hand.Index_finger.components[0].setCurrentAngle(5,self.left_arm.hand.Index_finger.components[0].vAxis)

        self.left_arm.hand.middle_finger.components[0].setCurrentAngle(-5,self.left_arm.hand.middle_finger.components[0].vAxis)

        self.left_arm.hand.ring_finger.components[0].setCurrentAngle(-90,self.left_arm.hand.ring_finger.components[0].uAxis)
        self.left_arm.hand.ring_finger.components[1].setCurrentAngle(-90,self.left_arm.hand.ring_finger.components[1].uAxis)
        self.left_arm.hand.ring_finger.components[2].setCurrentAngle(-90,self.left_arm.hand.ring_finger.components[2].uAxis)

        self.left_arm.hand.little_finger.components[0].setCurrentAngle(-90,self.left_arm.hand.little_finger.components[0].uAxis)
        self.left_arm.hand.little_finger.components[1].setCurrentAngle(-90,self.left_arm.hand.little_finger.components[1].uAxis)
        self.left_arm.hand.little_finger.components[2].setCurrentAngle(-90,self.left_arm.hand.little_finger.components[2].uAxis) 

    def test_case_3(self):
        # Right arm
        self.right_arm.limb.components[0].setCurrentAngle(-120,self.right_arm.limb.components[0].vAxis)
        self.right_arm.limb.components[1].setCurrentAngle(-45,self.right_arm.limb.components[1].vAxis)
        self.right_arm.limb.components[1].setCurrentAngle(90,self.right_arm.limb.components[1].wAxis)
        self.right_arm.limb.components[2].setCurrentAngle(-30,self.right_arm.limb.components[2].uAxis)
        self.right_arm.limb.components[3].setCurrentAngle(-30,self.right_arm.limb.components[3].uAxis)
        # Right arm
        self.right_arm.hand.wrist.setCurrentAngle(-30,self.right_arm.hand.wrist.uAxis)
        self.right_arm.hand.palm.setCurrentAngle(-30,self.right_arm.hand.wrist.uAxis)

        # Left arm
        self.left_arm.limb.components[0].setCurrentAngle(120,self.left_arm.limb.components[0].vAxis)
        self.left_arm.limb.components[1].setCurrentAngle(45,self.left_arm.limb.components[1].vAxis)
        self.left_arm.limb.components[1].setCurrentAngle(-90,self.left_arm.limb.components[1].wAxis)
        self.left_arm.limb.components[2].setCurrentAngle(-30,self.left_arm.limb.components[2].uAxis)
        self.left_arm.limb.components[3].setCurrentAngle(-30,self.left_arm.limb.components[3].uAxis)
        # Left hand
        self.left_arm.hand.wrist.setCurrentAngle(-30,self.left_arm.hand.wrist.uAxis)
        self.left_arm.hand.palm.setCurrentAngle(-30,self.left_arm.hand.wrist.uAxis)

        # Chest
        self.chest.setCurrentAngle(20,self.chest.vAxis)

        # Head
        self.head.neck.setCurrentAngle(-10,self.head.neck.vAxis)
        self.head.head.setCurrentAngle(-10,self.head.head.vAxis)

    def test_case_4(self):
        # Head
        self.head.neck.setCurrentAngle(60,self.head.neck.wAxis)
        self.head.head.setCurrentAngle(-15,self.head.head.uAxis)

        # Chest
        self.chest.setCurrentAngle(20,self.chest.vAxis)

        # Right arm
        self.right_arm.limb.components[0].setCurrentAngle(-75,self.right_arm.limb.components[0].vAxis)
        self.right_arm.limb.components[1].setCurrentAngle(0,self.right_arm.limb.components[1].vAxis)
        self.right_arm.limb.components[1].setCurrentAngle(90,self.right_arm.limb.components[1].wAxis)
        self.right_arm.limb.components[2].setCurrentAngle(-75,self.right_arm.limb.components[2].uAxis)
        self.right_arm.limb.components[3].setCurrentAngle(-75,self.right_arm.limb.components[3].uAxis)

        # Left arm
        self.left_arm.limb.components[0].setCurrentAngle(105,self.left_arm.limb.components[0].vAxis)
        self.left_arm.limb.components[1].setCurrentAngle(0,self.left_arm.limb.components[1].vAxis)

        # Right leg
        self.right_leg.limb.components[0].setCurrentAngle(-60,self.right_leg.limb.components[0].vAxis)
        self.right_leg.limb.components[1].setCurrentAngle(-15,self.right_leg.limb.components[1].vAxis)
        self.right_leg.limb.components[1].setCurrentAngle(90,self.right_leg.limb.components[1].wAxis)
        self.right_leg.limb.components[2].setCurrentAngle(45,self.right_leg.limb.components[2].uAxis)
        self.right_leg.limb.components[3].setCurrentAngle(45,self.right_leg.limb.components[3].uAxis)

        # Right foot
        self.right_leg.foot.setCurrentAngle(-10,self.right_leg.foot.uAxis)

        # Left leg
        self.left_leg.limb.components[0].setCurrentAngle(60,self.left_leg.limb.components[0].vAxis)
        self.left_leg.limb.components[1].setCurrentAngle(0,self.left_leg.limb.components[1].vAxis)

        # Left foot
        self.left_leg.ankle.setCurrentAngle(-10,self.left_leg.ankle.vAxis)
        self.left_leg.foot.setCurrentAngle(-10,self.left_leg.foot.vAxis)
    

    def test_case_5(self):
        # Right arm
        self.right_arm.limb.components[0].setCurrentAngle(-30,self.right_arm.limb.components[0].uAxis)
        self.right_arm.limb.components[1].setCurrentAngle(0,self.right_arm.limb.components[1].wAxis)
        self.right_arm.limb.components[2].setCurrentAngle(-45,self.right_arm.limb.components[2].uAxis)
        self.right_arm.limb.components[3].setCurrentAngle(-45,self.right_arm.limb.components[3].uAxis)
        self.right_arm.hand.wrist.setCurrentAngle(-90,self.right_arm.hand.wrist.wAxis)

        # Left arm
        self.left_arm.limb.components[0].setCurrentAngle(60,self.left_arm.limb.components[0].uAxis)
        self.left_arm.limb.components[1].setCurrentAngle(0,self.left_arm.limb.components[1].wAxis)
        self.left_arm.limb.components[2].setCurrentAngle(-45,self.left_arm.limb.components[2].uAxis)
        self.left_arm.limb.components[3].setCurrentAngle(-45,self.left_arm.limb.components[3].uAxis)
        self.left_arm.hand.wrist.setCurrentAngle(90,self.left_arm.hand.wrist.wAxis)

        # Right leg
        self.right_leg.limb.components[0].setCurrentAngle(45,self.right_leg.limb.components[0].uAxis)
        self.right_leg.limb.components[2].setCurrentAngle(30,self.right_leg.limb.components[2].uAxis)
        self.right_leg.limb.components[3].setCurrentAngle(30,self.right_leg.limb.components[3].uAxis)

        # Left leg
        self.left_leg.limb.components[0].setCurrentAngle(-90,self.left_leg.limb.components[0].uAxis)
        self.left_leg.limb.components[2].setCurrentAngle(30,self.left_leg.limb.components[2].uAxis)
        self.left_leg.limb.components[3].setCurrentAngle(30,self.left_leg.limb.components[3].uAxis)

    