"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA3
due date:                   Nov.09,2021

Added 2 prey creatures, prey_battery, and 1 predator creature, predator_robot, in init() of Vivarium class.
Added addfood() method to add food particle randomly in the tank.
"""

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
from ModelTank import Tank
from ModelLinkage import predator_robot, prey_battery, food
from EnvironmentObject import EnvironmentObject


class Vivarium(Component, Animation):
    """
    The Vivarium for our animation
    """
    components = None  # List
    parent = None  # class that have current context
    tank = None
    tank_dimensions = None

    ##### BONUS 5(TODO 5 for CS680 Students): Feed your creature
    # Requirements:
    #   Add chunks of food to the vivarium which can be eaten by your creatures.
    #     * When ‘f’ is pressed, have a food particle be generated at random within the vivarium.
    #     * Be sure to draw the food on the screen with an additional model. It should drop slowly to the bottom of
    #     the vivarium and remain there within the tank until eaten.
    #     * The food should disappear once it has been eaten. Food is eaten by the first creature that touches it.

    def __init__(self, parent):
        self.parent = parent

        self.tank_dimensions = [4, 4, 4]
        tank = Tank(parent, self.tank_dimensions)
        super(Vivarium, self).__init__(Point((0, 0, 0)))

        # Build relationship
        self.addChild(tank)
        self.tank = tank

        # Store all components in one list, for us to access them later
        self.components = [tank]

        #self.addNewObjInTank(food(parent, Point([self.tank_dimensions[i]/2 * (random.random() - 0.5) for i in range(3)])))

        self.addNewObjInTank(prey_battery(parent, Point([self.tank_dimensions[i]/2 * (random.random() - 0.5) for i in range(3)])))
        self.addNewObjInTank(prey_battery(parent, Point([self.tank_dimensions[i]/2 * (random.random() - 0.5) for i in range(3)])))
        # self.addNewObjInTank(prey_battery(parent, Point([self.tank_dimensions[i]/2 * (random.random() - 0.5) for i in range(3)])))
        # self.addNewObjInTank(prey_battery(parent, Point([self.tank_dimensions[i]/2 * (random.random() - 0.5) for i in range(3)])))
        # self.addNewObjInTank(prey_battery(parent, Point([self.tank_dimensions[i]/2 * (random.random() - 0.5) for i in range(3)])))

        # self.addNewObjInTank(predator_robot(parent, Point([self.tank_dimensions[i]/2 * (random.random() - 0.5) for i in range(3)])))
        # self.addNewObjInTank(predator_robot(parent, Point([self.tank_dimensions[i]/2 * (random.random() - 0.5) for i in range(3)])))

    def animationUpdate(self):
        """
        Update all creatures in vivarium
        """
        for c in self.components[::-1]:
            if isinstance(c, Animation):
                c.animationUpdate()

    def delObjInTank(self, obj):
        if isinstance(obj, Component):
            self.tank.children.remove(obj)
            self.components.remove(obj)
            del obj

    def addNewObjInTank(self, newComponent):
        if isinstance(newComponent, Component):
            self.tank.addChild(newComponent)
            self.components.append(newComponent)
        if isinstance(newComponent, EnvironmentObject):
            # add environment components list reference to this new object's
            newComponent.env_obj_list = self.components

    def addfood(self):
        # release the food randomly in the central region of the tank
        f = food(self.parent, Point([self.tank_dimensions[i]/2 * (random.random() - 0.5) for i in range(3)]))
        f.initialize()
        self.addNewObjInTank(f)
