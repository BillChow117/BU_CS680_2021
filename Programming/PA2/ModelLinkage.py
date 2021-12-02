"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""

from Component import Component
from ModelFinger import ModelFinger
from Point import Point
import ColorType as Ct
from DisplayableCube import DisplayableCube


class ModelLinkage(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature. 

    components = None
    contextParent = None

    def __init__(self, parent, position, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        linkageLength = 0.5
        link1 = Component(Point((0, 0, 0)), DisplayableCube(self.contextParent, 1, [0.2, 0.2, 0.5]))
        link1.setDefaultColor(Ct.DARKORANGE1)
        link1.setDefaultAngle(90, link1.vAxis)
        link2 = Component(Point((0, 0, linkageLength)), DisplayableCube(self.contextParent, 1, [0.2, 0.2, linkageLength]))
        link2.setDefaultColor(Ct.DARKORANGE2)
        link3 = Component(Point((0, 0, linkageLength)), DisplayableCube(self.contextParent, 1, [0.2, 0.2, linkageLength]))
        link3.setDefaultColor(Ct.DARKORANGE3)
        link4 = Component(Point((0, 0, linkageLength)), DisplayableCube(self.contextParent, 1, [0.2, 0.2, linkageLength]))
        link4.setDefaultColor(Ct.DARKORANGE4)

        self.addChild(link1)
        link1.addChild(link2)
        link2.addChild(link3)
        link3.addChild(link4)

        finger = ModelFinger(self.contextParent,Point((0,0,0)))
        finger.rotate(-90,finger.vAxis)
        self.addChild(finger)

        self.components = [link1, link2, link3, link4] + finger.components

