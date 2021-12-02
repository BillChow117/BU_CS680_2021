'''
Define Our class which is stores collision detection and environment information here
Created on Nov 1, 2018

:author: micou(Zezhou Sun)
:version: 2021.1.1
'''

from Point import Point


class EnvironmentObject:
    """
    Define properties and interface for a object in our environment
    """
    bound_center = None  # Point
    bound_radius = 0  # float
    env_obj_list = None  # list<Environment>
    species_id = 0  # species with larger id number will prey species with small number

    def __init__(self):
        """
        Init all variables.
        env_obj_list is used to store all components in environment for this creature to interact with
        bound_center and bound_radius defines collision detection for this object
        species_id defines this object's role in the food chain
        """
        self.env_obj_list = []
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0
        self.species_id = 0

    def addCollisionObj(self, a):
        """
        Add an environment object for this creature to interact with
        """
        if isinstance(a, EnvironmentObject):
            self.env_obj_list.append(a)

    def rmCollisionObj(self, a):
        """
        Remove an environment object for this creature to interact with
        """
        if isinstance(a, EnvironmentObject):
            self.env_obj_list.remove(a)
