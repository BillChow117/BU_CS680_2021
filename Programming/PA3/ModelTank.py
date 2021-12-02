"""
All creatures should be added to Vivarium. Some help functions to add/remove creature are defined here.
Created on 20181028

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import random

from Point import Point
from Component import Component
from Animation import Animation
from DisplayableTank import DisplayableTank
from EnvironmentObject import EnvironmentObject


class Tank(Component, EnvironmentObject):
    tank_dimensions = None

    def __init__(self, parent, tank_dimensions):
        self.tank_dimensions = tank_dimensions
        self.species_id = -1
        super(Tank, self).__init__(Point((0, 0, 0)), DisplayableTank(parent, *self.tank_dimensions))
