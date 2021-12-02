"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA3
due date:                   Nov.09,2021

Linkage class:  The parent class for creatures. 
                Added build_model() method to build the creature.
                Divided animationUpdate() method into 4 parts: 
                animation(), translation(), rotation() and group_behavior().
                Its child class should implement build_model() and animation() method, and 
                optionally for translation(), rotation() and group_behavior().
            
food class:     The food particle class, child class of Linkage class, overrided the translation() method to simplely sink to the bottom of tank.

prey_battery class: The prey creature class, child class of Linkage class. The predator_robot creature would chase it.

predator_robot class:   The predator creature class, child class of Linkage class. The modle was imported from PA2.
"""

"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""
import random
import copy
import numpy as np
import math

from wx.core import ComboPopup
from Component import Component
from Point import Point
import ColorType as CT
from Displayable import Displayable
from Animation import Animation
from EnvironmentObject import EnvironmentObject
from Quaternion import Quaternion
from Vivarium import Tank
from DisplayableCube import DisplayableCube
from DisplayableCylinder import DisplayableCylinder
from DisplayableTrapezoid import DisplayableTrapezoid
from DisplayableSphere import DisplayableSphere
from ModelHead import ModelHead
from ModelArm import ModelArm
from ModelLeg import ModelLeg
from ModelPropeller import ModelPropeller

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")


class ModelLinkage(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, linkageLength=0.5, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        link1 = Component(Point((0, 0, 0)),
                          DisplayableCube(self.contextParent, 1, [linkageLength / 4, linkageLength / 4, linkageLength]))
        link1.setDefaultColor(CT.DARKORANGE1)
        link2 = Component(Point((0, 0, linkageLength)),
                          DisplayableCube(self.contextParent, 1, [linkageLength / 4, linkageLength / 4, linkageLength]))
        link2.setDefaultColor(CT.DARKORANGE2)
        link3 = Component(Point((0, 0, linkageLength)),
                          DisplayableCube(self.contextParent, 1, [linkageLength / 4, linkageLength / 4, linkageLength]))
        link3.setDefaultColor(CT.DARKORANGE3)
        link4 = Component(Point((0, 0, linkageLength)),
                          DisplayableCube(self.contextParent, 1, [linkageLength / 4, linkageLength / 4, linkageLength]))
        link4.setDefaultColor(CT.DARKORANGE4)

        self.addChild(link1)
        link1.addChild(link2)
        link2.addChild(link3)
        link3.addChild(link4)

        self.components = [link1, link2, link3, link4]


class DisplayableCube(Displayable):
    """
    Create a enclosed cylinder whose one end is at z=0 and it grows along z coordinates
    """

    callListHandle = 0  # long int. override the one in Displayable
    qd = None  # Quadric
    scale = None
    edgeLength = 1
    _bufferData = None

    def __init__(self, parent, edgeLength, scale=None):
        super().__init__(parent)
        parent.context.SetCurrent(parent)
        self.edgeLength = edgeLength
        if scale is None:
            scale = [1, 1, 1]
        self.scale = scale

    def draw(self):
        gl.glCallList(self.callListHandle)

    def initialize(self):
        self.callListHandle = gl.glGenLists(1)
        self.qd = glu.gluNewQuadric()

        v_l = [
            [-self.edgeLength / 2, -self.edgeLength / 2, -self.edgeLength / 2],
            [self.edgeLength / 2, -self.edgeLength / 2, -self.edgeLength / 2],
            [self.edgeLength / 2, self.edgeLength / 2, -self.edgeLength / 2],
            [- self.edgeLength / 2, self.edgeLength / 2, -self.edgeLength / 2],
            [- self.edgeLength / 2, -self.edgeLength / 2, self.edgeLength / 2],
            [self.edgeLength / 2, -self.edgeLength / 2, self.edgeLength / 2],
            [self.edgeLength / 2, self.edgeLength / 2, self.edgeLength / 2],
            [- self.edgeLength / 2, self.edgeLength / 2, self.edgeLength / 2],
        ]

        gl.glNewList(self.callListHandle, gl.GL_COMPILE)
        gl.glPushMatrix()

        gl.glScale(*self.scale)
        gl.glTranslate(0, 0, self.edgeLength / 2)

        # a primitive cube
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex3f(*v_l[1])
        gl.glVertex3f(*v_l[0])
        gl.glVertex3f(*v_l[3])
        gl.glVertex3f(*v_l[2])

        gl.glVertex3f(*v_l[4])
        gl.glVertex3f(*v_l[5])
        gl.glVertex3f(*v_l[6])
        gl.glVertex3f(*v_l[7])

        gl.glVertex3f(*v_l[0])
        gl.glVertex3f(*v_l[4])
        gl.glVertex3f(*v_l[7])
        gl.glVertex3f(*v_l[3])

        gl.glVertex3f(*v_l[7])
        gl.glVertex3f(*v_l[6])
        gl.glVertex3f(*v_l[2])
        gl.glVertex3f(*v_l[3])

        gl.glVertex3f(*v_l[5])
        gl.glVertex3f(*v_l[1])
        gl.glVertex3f(*v_l[2])
        gl.glVertex3f(*v_l[6])

        gl.glVertex3f(*v_l[0])
        gl.glVertex3f(*v_l[1])
        gl.glVertex3f(*v_l[5])
        gl.glVertex3f(*v_l[4])

        gl.glEnd()

        gl.glPopMatrix()
        gl.glEndList()


##### TODO 1: Construct your two different creatures
# Requirements:
#   1. For the basic parts of your creatures, feel free to use routines provided with the previous assignment.
#   You are also free to create your own basic parts, but they must be polyhedral (solid).
#   2. The creatures you design should have moving linkages of the basic parts: legs, arms, wings, antennae,
#   fins, tentacles, etc.
#   3. Model requirements:
#         1. Predator: At least one (1) creature. Should have at least two moving parts in addition to the main body
#         2. Prey: At least two (2) creatures. The two prey can be instances of the same design. Should have at
#         least one moving part.
#         3. The predator and prey should have distinguishable different colors.
#         4. You are welcome to reuse your PA2 creature in this assignment.

class Linkage(Component, Animation, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    parent = None
    components = None
    rotation_speed = None
    translation_speed = None        # the speed direction
    velocity = None                 # the speed scale

    def __init__(self, parent, position):
        super(Linkage, self).__init__(position)
        self.parent = parent
        self.components = []
        self.rotation_speed = []
        self.UpVector = Point((0,1,0))
        self.last_translation_speed = Point((0,1,0))
        self.viewing_quaternion = Quaternion()
        self.translation_speed = Point([random.random() - 0.5 for _ in range(3)]).normalize()
        #self.translation_speed = Point((1,0,0))
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.5
        self.species_id = 1
        self.velocity = 0.02

    def build_model(self):
        """
        Called when need to build the model
        """
        raise NotImplementedError("build_model method not implemented yet")

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create period animation for creature joints
        self.animation()

        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between it and tank walls. When it hits with tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.

        # then we translate our creature

        # save the last translation speed for rotation() method
        self.translation()

        ##### TODO 4: Eyes on the road!
        # Requirements:
        #   1. CCreatures should face in the direction they are moving. For instance, a fish should be facing the
        #   direction in which it swims. Remember that we require your creatures to be movable in 3 dimensions,
        #   so they should be able to face any direction in 3D space.
        self.rotation()

        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.
        self.group_behavior()

        self.update()

    def animation(self):
        """
        Called when need to update the animation
        """
        raise NotImplementedError("animation method not implemented yet")

    def translation(self):
        # overall translate intention
        overall_v = Point((0,0,0))
        
        # then this is our vivarium tank, do wall collision detection
        tank_d = self.parent.vivarium.tank_dimensions
        # reflect when it is going to hit the wall in next frame
        if not ((tank_d[0] / 2 - self.bound_radius) >
                (self.current_position[0] + self.translation_speed[0] * self.velocity) >
                (-tank_d[0] / 2 + self.bound_radius)):
            self.translation_speed.coords[0] *= -1
            # Collision detection has a higher priority
            self.current_position += self.translation_speed * self.velocity
            return
        if not ((tank_d[1] / 2 - self.bound_radius) >
                (self.current_position[1] + self.translation_speed[1] * self.velocity) >
                (-tank_d[1] / 2 + self.bound_radius)):
            self.translation_speed.coords[1] *= -1
            # Collision detection has a higher priority
            self.current_position += self.translation_speed * self.velocity
            return
        if not ((tank_d[2] / 2 - self.bound_radius) >
                (self.current_position[2] + self.translation_speed[2] * self.velocity) >
                (-tank_d[2] / 2 + self.bound_radius)):
            self.translation_speed.coords[2] *= -1
            # Collision detection has a higher priority
            self.current_position += self.translation_speed * self.velocity
            return
        
        # build the wall a surface potential field when close enough, so the item will avoid hitting the wall
        dis = (tank_d[0] / 2 - self.bound_radius) - (self.current_position[0] + self.translation_speed[0] * self.velocity)
        if ( dis < tank_d[0] / 20):
            overall_v += Point((-1,0,0)) * (1/(dis**2 + 0.2))

        dis = (self.current_position[0] + self.translation_speed[0] * self.velocity) - (-tank_d[0] / 2 + self.bound_radius)
        if ( dis < tank_d[0] / 20):
            overall_v += Point((1,0,0)) * (1/(dis**2 + 0.2))
        
        dis = (tank_d[1] / 2 - self.bound_radius) - (self.current_position[1] + self.translation_speed[1] * self.velocity)
        if ( dis < tank_d[1] / 20):
            overall_v += Point((0,-1,0)) * (1/(dis**2 + 0.2))

        dis = (self.current_position[1] + self.translation_speed[1] * self.velocity) - (-tank_d[1] / 2 + self.bound_radius)
        if ( dis < tank_d[1] / 20):
            overall_v += Point((0,1,0)) * (1/(dis**2 + 0.2))

        dis = (tank_d[2] / 2 - self.bound_radius) - (self.current_position[2] + self.translation_speed[2] * self.velocity)
        if ( dis < tank_d[2] / 20):
            overall_v += Point((0,0,-1)) * (1/(dis**2 + 0.2))

        dis = (self.current_position[2] + self.translation_speed[2] * self.velocity) - (-tank_d[2] / 2 + self.bound_radius)
        if ( dis < tank_d[2] / 20):
            overall_v += Point((0,0,1)) * (1/(dis**2 + 0.2))

        
        for item in self.env_obj_list:
            if item is not self and item is not self.parent.vivarium.tank:
                # this is other object

                # the vector between two object
                v = item.current_position - self.current_position
                nv = v.normalize()
                distance_square = np.sum(np.square(v.coords))
                distance = math.sqrt(distance_square)

                # Collision
                if distance <= item.bound_radius + self.bound_radius:

                    # same speice: reflect
                    if self.species_id == item.species_id:
                    
                        # the surface normal vector of the reflect plane
                        self.translation_speed = (self.translation_speed.reflect(nv)).normalize()

                        # Collision detection has a higher priority
                        self.current_position += self.translation_speed * self.velocity
                        return

                    # eat the prey or food
                    elif self.species_id > item.species_id: 
                        
                        # remove the item from vivarium
                        self.parent.vivarium.delObjInTank(item)

                        # the last frame of the item would remain if not calling the update() method
                        self.parent.update()

                # chasing and escaping
                else:
                    if self.species_id > item.species_id:
                        overall_v += nv * (1/distance_square)
                    elif self.species_id < item.species_id:
                        overall_v -= nv * (1/distance_square)


        self.translation_speed += overall_v.normalize()
        self.translation_speed = self.translation_speed.normalize()
        self.current_position += self.translation_speed * self.velocity

    def rotation(self):
        '''
        Quaterion: dosen't work
        '''
        # theta = max(min(self.last_translation_speed.dot(self.translation_speed),1),-1)
        # theta = math.acos(theta)
        # if theta == math.pi:
        #     for n in [Point((1,0,0)),Point((0,1,0)),Point((0,0,1)),Point((-1,0,0)),Point((0,-1,0)),Point((0,0,-1))]:
        #         if not self.last_translation_speed.directionEq(n):
        #             rotate_axis = self.last_translation_speed.cross3d(n).normalize()
        # else:
        #     rotate_axis = self.translation_speed.cross3d(self.last_translation_speed).normalize()
        # print(theta * 180 / math.pi,rotate_axis.getCoords(),rotate_axis.getLength())
        # c = math.cos(0.5 * theta)
        # s = math.sin(0.5 * theta)
        # q = Quaternion(c,s * rotate_axis[0],s * rotate_axis[1], s * rotate_axis[2])
        # self.viewing_quaternion = q.multiply(self.viewing_quaternion)
        # self.viewing_quaternion.normalize()
        # self.pre_rotation_matrix = self.viewing_quaternion.toMatrix()
        # self.last_translation_speed = self.translation_speed.copy()

        '''
        Local coordinate
        '''
        # build the local coordinates bases
        w = self.translation_speed.normalize()
        u = self.UpVector.cross3d(self.translation_speed).normalize()
        v = w.cross3d(u).normalize()

        # build the rotation matirx
        rotation_matrix = np.array([[u[0],u[1],u[2],0],\
                                    [v[0],v[1],v[2],0],\
                                    [w[0],w[1],w[2],0],\
                                    [0,0,0,1]])

        # feed to post_rotation_matrix to rotate
        self.post_rotation_matrix = rotation_matrix

    def group_behavior(self):

        # parameter to center together
        self.centeringFactor = 0.05
        self.visualRange = 2

        # parameter to avoid others
        self.minDis = 0.1
        self.avoidFactor = 0.1

        # get center coords
        for item in self.env_obj_list:
            center = Point((0,0,0))
            avoid = Point((0,0,0))
            numNeighbors = 0
            if item is not self and item is not self.parent.vivarium.tank and self.species_id == item.species_id:
                # the vector between two object
                v = item.current_position - self.current_position
                nv = v.normalize()
                distance_square = np.sum(np.square(v.coords))
                distance = math.sqrt(distance_square)

                # the same speice creature is in the visual range
                if distance < self.visualRange:
                    center += item.current_position
                    numNeighbors += 1

                # the creature is too close
                if distance - self.bound_radius - item.bound_radius < self.minDis:
                    avoid += self.current_position - item.current_position

        if numNeighbors:
            center *= 1/numNeighbors
        
        # centering
        self.translation_speed += (center - self.current_position) * self.centeringFactor + avoid * self.avoidFactor
        self.translation_speed.normalize()


class food(Linkage):

    def __init__(self, parent, position):
        super().__init__(parent, position)
        self.species_id = 0
        self.velocity = 0.01
        self.bound_radius = 0.1
        self.UpVector = Point((0,1,0)).normalize()
        self.translation_speed = Point((0,-1,0)).normalize()
        self.last_translation_speed = Point((0,-1,0)).normalize()
        self.build_model()
    
    def build_model(self):
        
        sphere = Component(Point((0,0,0)),DisplayableSphere(self.parent,1,(0.05,0.05,0.05)))
        sphere.setDefaultColor(CT.RED)
        self.addChild(sphere)
        self.components = [sphere]

    def translation(self):
        # then this is our vivarium tank, do wall collision detection
        tank_d = self.parent.vivarium.tank_dimensions

        if not ((self.current_position[1] + self.translation_speed[1] * self.velocity) > (-tank_d[1] / 2 + self.bound_radius)):
            # stop when sink to the bottom
            # self.current_position += self.translation_speed * self.velocity
            self.translation_speed.setCoords((0,0,0))
            return

        self.current_position += self.translation_speed * self.velocity

    def rotation(self):
        pass

    def animation(self):
        pass

    def group_behavior(self):
        pass

class prey_battery(Linkage):


    def __init__(self, parent, position):
        super().__init__(parent, position)
        self.species_id = 1
        self.velocity = 0.02
        self.bound_radius = 0.2
        self.UpVector = Point((0,1,0)).normalize()
        #self.translation_speed = Point((0,-1,0)).normalize()
        self.last_translation_speed = Point((0,0,1)).normalize()
        self.build_model()

    def build_model(self):

        battery = Component(Point((0,0,0)),DisplayableCylinder(self.parent,1,1,4,(0.5,0.5,1)))
        battery.setDefaultColor(CT.GREEN)

        propeller1 = Component(Point((0,0,0)),DisplayableCube(self.parent,1,(0.4,4,0.2)))
        propeller1.setDefaultColor(CT.GREEN)

        propeller2 = Component(Point((0,0,0)),DisplayableCube(self.parent,1,(0.4,4,0.2)))
        propeller2.setDefaultAngle(120,propeller2.wAxis)
        propeller2.setDefaultColor(CT.GREEN)

        propeller3 = Component(Point((0,0,0)),DisplayableCube(self.parent,1,(0.4,4,0.2)))
        propeller3.setDefaultAngle(240,propeller3.wAxis)
        propeller3.setDefaultColor(CT.GREEN)

        self.addChild(battery)
        battery.addChild(propeller1)
        battery.addChild(propeller2)
        battery.addChild(propeller3)
        self.setDefaultScale((0.05,0.05,0.05))
        self.components = [battery,propeller1,propeller2,propeller3]

    def animation(self):
        self.wAngle = (self.wAngle + 10) % 360       

class predator_robot(Linkage):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """

    def __init__(self, parent, position):
        super().__init__(parent, position)
        self.species_id = 2
        self.velocity = 0.01
        self.bound_radius = 0.4
        self.UpVector = Point((0,1,0)).normalize()
        #self.translation_speed = Point((0,1,1)).normalize()
        self.last_translation_speed = Point((0,0,1)).normalize()
        self.build_model()

    def build_model(self):

        chest_top_edge = 5
        chest_bot_edge = 3
        chest_len = 3
        chest_scale=(-1,0.3,-1)

        # Build a fixed waist
        waist_edge = 2 * chest_bot_edge
        waist_scale = (0.5,0.3,0.5)
        waist = Component(Point((0,0,0)),DisplayableCube(self.parent,waist_edge,waist_scale))
        waist.setDefaultColor(CT.ORANGE)
        waist.setDefaultAngle(90,waist.uAxis)
        waist.setRotateExtent(waist.uAxis,90,90)
        waist.setRotateExtent(waist.vAxis,0,0)
        waist.setRotateExtent(waist.wAxis,0,0)
        self.addChild(waist)
        self.components.append(waist)
        self.waist = waist

        # Build a chest
        chest = Component(Point((0,0,chest_bot_edge/3)),DisplayableTrapezoid(self.parent,chest_top_edge,chest_bot_edge,chest_len,chest_scale))
        chest.setDefaultColor(CT.ORANGE)
        chest.setRotateExtent(chest.uAxis,-30,60)
        chest.setRotateExtent(chest.vAxis,-10,10)
        chest.setRotateExtent(chest.wAxis,-45,45)
        waist.addChild(chest)
        self.components.append(chest)
        self.chest = chest

        # Build a head
        head = ModelHead(self.parent,Point((0,0,-2*chest_len)))
        chest.addChild(head)
        self.components += head.components
        self.head = head

        # Two rocket prepellers on the back
        right_prepeller = ModelPropeller(self.parent,Point((-chest_top_edge/3,-chest_top_edge*chest_scale[1],3/2*chest_len*chest_scale[2])))
        right_prepeller.joint.setDefaultAngle(30,right_prepeller.joint.uAxis)
        right_prepeller.joint.setRotateDirection(1,-1)
        right_prepeller.joint.setRotateDirection(2,-1)
        right_prepeller.joint.setRotateExtent(right_prepeller.joint.uAxis,30,150)
        right_prepeller.joint.setRotateExtent(right_prepeller.joint.vAxis,-90,5)
        right_prepeller.joint.setRotateExtent(right_prepeller.joint.wAxis,0,0)
        chest.addChild(right_prepeller)
        self.right_prepeller = right_prepeller
        self.components += right_prepeller.components

        left_prepeller = ModelPropeller(self.parent,Point((chest_top_edge/3,-chest_top_edge*chest_scale[1],3/2*chest_len*chest_scale[2])))
        left_prepeller.joint.setDefaultAngle(30,left_prepeller.joint.uAxis)
        left_prepeller.joint.setRotateExtent(left_prepeller.joint.uAxis,30,150)
        left_prepeller.joint.setRotateExtent(left_prepeller.joint.vAxis,-5,90)
        left_prepeller.joint.setRotateExtent(left_prepeller.joint.wAxis,0,0)
        chest.addChild(left_prepeller)
        self.left_prepeller = left_prepeller
        self.components += left_prepeller.components

        # Build the right arm
        right_arm = ModelArm(self.parent,Point((-(chest_top_edge*2/3 + chest_bot_edge/3),0,-2*2/3*chest_len)),True)
        
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
        left_arm = ModelArm(self.parent,Point((chest_top_edge*2/3 + chest_bot_edge/3,0,-2*2/3*chest_len)),False)
        chest.addChild(left_arm)
        self.components += left_arm.components
        self.left_arm = left_arm

        curr_waist_edge_x = waist_edge * waist_scale[0]
        curr_waist_edge_y = waist_edge * waist_scale[1]
        curr_waist_edge_z = waist_edge * waist_scale[2]


        # Build the right leg
        right_leg = ModelLeg(self.parent,Point((-curr_waist_edge_x/2,0,curr_waist_edge_z*3/4)),True)
        
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
        left_leg = ModelLeg(self.parent,Point((curr_waist_edge_x/2,0,curr_waist_edge_z*3/4)),False)
        waist.addChild(left_leg)
        self.components += left_leg.components
        self.left_leg =left_leg

        # set a scale to fit the robot in the tank
        self.setDefaultScale((0.03,0.03,0.03))

        # for animation
        self.animeComp = [self.right_arm.limb.components[0],\
                            self.left_arm.limb.components[0],\
                            self.right_leg.limb.components[0],\
                            self.left_leg.limb.components[0]]

        for comp in self.animeComp:
            comp.setRotateExtent(comp.uAxis, -40, 40)

        # right arm
        self.rotation_speed.append([1,0,0])
        # left arm
        self.rotation_speed.append([-1,0,0])
        # right leg
        self.rotation_speed.append([-1,0,0])
        # left leg
        self.rotation_speed.append([1,0,0])

    def animation(self):
        for i, comp in enumerate(self.animeComp):
            comp.rotate(self.rotation_speed[i][0]*3, comp.uAxis)
            comp.rotate(self.rotation_speed[i][1]*3, comp.vAxis)
            comp.rotate(self.rotation_speed[i][2]*3, comp.wAxis)
            if comp.uAngle in comp.uRange:  # rotation reached the limit
                self.rotation_speed[i][0] *= -1
            if comp.vAngle in comp.vRange:
                self.rotation_speed[i][1] *= -1
            if comp.wAngle in comp.wRange:
                self.rotation_speed[i][2] *= -1
