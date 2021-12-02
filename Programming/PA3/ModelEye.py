"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA2
due date:                   Oct.12,2021

Head class: Draw a sphere eye ball with a sphere pupil
"""

from Component import Component
from Point import Point
import ColorType as CT
from DisplayableSphere import DisplayableSphere


class ModelEye(Component):
    components = None
    contextParent = None

    def __init__(self, parent, position, eye_radius = 0.4, scale = None, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        pupil_radius = eye_radius / 3

        eye = Component(Point((0,0,0)),DisplayableSphere(self.contextParent,eye_radius))
        eye.setDefaultColor(CT.SILVER)
        self.addChild(eye)
        self.eye = eye
        self.components.append(eye)
        
        pupil = Component(Point((0,-eye_radius,0)),DisplayableSphere(self.contextParent,pupil_radius))
        pupil.setDefaultColor(CT.BLUE)
        eye.addChild(pupil)
        self.pupil = pupil

        if scale != None:
            self.setDefaultScale(scale)




