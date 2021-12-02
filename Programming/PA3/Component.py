"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA3
due date:                   Nov.09,2021

Added setRotateDirection() method in class. Because it is used in PA2 to implement the robto modle.
"""

'''
Created on 20181021

@author: Zezhou Sun
@description: Define Component object. 
'''
import copy
import math
import numpy as np

from Point import Point
from ColorType import ColorType
from Displayable import Displayable
from Quaternion import Quaternion

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


class Component:
    children = None  # list

    display_obj = None  # inherit from Displayable
    callListHandle = None  # ctype.c_uint used to link to generated openGL list

    default_color = None  # ColorType
    current_color = None  # ColorType
    default_position = None  # Point
    current_position = None  # Point
    default_scale = None  # list
    current_scale = None  # list

    uAxis = None  # list<float>(3): local basis u
    vAxis = None  # list<float>(3): local basis v
    wAxis = None  # list<float>(3): local basis w

    default_uAngle = 0.0
    uAngle = 0.0
    uRange = None  # list<float>(2)
    default_vAngle = 0.0
    vAngle = 0.0
    vRange = None  # list<float>(2)
    default_wAngle = 0.0
    wAngle = 0.0
    wRange = None  # list<float>(2)
    axisBucket = None

    pre_rotation_matrix = None
    post_rotation_matrix = None

    def __init__(self, position, display_obj=None):
        """
                Init Component

                :param position: This component's relative translation from the parent's origin to its origin
                :type position: Point
                :param display_obj: The displayable object to be assigned to this component. If no Displayable object is given, then this Component has nothing to draw
                :type display_obj: Displayable
                :rtype: None
                """
        # list variable initialization should be done here. Otherwise list variable in different instances will share
        # the same list
        self.children = []
        self.uAxis = [1, 0, 0]
        self.vAxis = [0, 1, 0]
        self.wAxis = [0, 0, 1]
        self.uRange = [-360, 360]
        self.vRange = [-360, 360]
        self.wRange = [-360, 360]
        self.rotate_direction = [1,1,1]
        self.axisBucket = [self.uAxis, self.vAxis, self.wAxis]

        # Type Checking
        if not isinstance(position, Point):
            raise TypeError("Incorrect Position, should have Point type")
        if not (isinstance(display_obj, Displayable) or isinstance(display_obj, type(None))):
            raise TypeError("display_obj can only accept None or Displayable object")

        # init some default values
        self.default_position = position.copy()
        self.current_position = position.copy()
        self.display_obj = display_obj
        self.default_color = ColorType(1, 1, 1)
        self.current_color = ColorType(1, 1, 1)
        self.default_scale = [1, 1, 1]
        self.current_scale = [1, 1, 1]
        self.pre_rotation_matrix = np.identity(4)
        self.post_rotation_matrix = np.identity(4)

    def addChild(self, child):
        """
        Add a child to this Component child list.

        :param child: The child Component to be added
        :type child: Component
        :return: None
        """
        # Basic TypeChecking
        if not isinstance(child, Component):
            raise TypeError("Children of a Component can only be Component")
        # Only add child when there is no duplicate child
        if child not in self.children:
            self.children.append(child)

    def initialize(self):
        """
        Initialize this component and all its children, compute the model and store in display list.
        This method is required if there is any parameter changed in the Component's Displayable objects

        :return: None
        """
        self.callListHandle = gl.glGenLists(1)

        if isinstance(self.display_obj, Displayable):
            self.display_obj.initialize()

        for c in self.children:
            c.initialize()

    def draw(self):
        """
        Render the model which is previously store in display list on canvas
        :return: None
        """
        gl.glCallList(self.callListHandle)

    def update(self):
        """
        Apply translation, rotation and scaling to this component and all its children
        :return: None
        """
        for c in self.children:
            c.update()

        gl.glNewList(self.callListHandle, gl.GL_COMPILE)
        gl.glPushMatrix()

        # translate and rotate to default_position we want
        gl.glTranslated(*self.current_position.getCoords())
        # last rotation before translation, can be used to control component's facing direction
        gl.glMultMatrixf(self.post_rotation_matrix)
        # rotation consists of euler rotation
        gl.glRotated(self.uAngle, *self.uAxis)
        gl.glRotated(self.vAngle, *self.vAxis)
        gl.glRotated(self.wAngle, *self.wAxis)
        # scale the object
        gl.glScale(*self.current_scale)
        # apply a rotation matrix to our component, this is useful if you want to set the default facing direction
        # of it before all the following transformation
        gl.glMultMatrixf(self.pre_rotation_matrix)

        # If this is a displayable component, draw it
        if isinstance(self.display_obj, Displayable):
            gl.glPushAttrib(gl.GL_CURRENT_BIT)
            gl.glColor3f(*self.current_color.getRGB())
            self.display_obj.draw()
            gl.glPopAttrib()

        # Draw all children inside matrix push and pop will make children inherit translation and rotation
        for c in self.children:
            c.draw()

        gl.glPopMatrix()
        gl.glEndList()
    
    def setRotateDirection(self,axis,direction):
        self.rotate_direction[axis] = direction / abs(direction)

    def rotate(self, degree, axis):
        """
        rotate along axis. axis should be one of this object's uAxis, vAxis, wAxis

        :param degree: rotate degree, in degs
        :type degree: float
        :param axis: rotation axis. Axis must be uAxis, vAxis, or wAxis
        :type axis: enum(self.uAxis, self.vAxis, self.wAxis)
        :return: None
        """

        def limit_rotation(input_degree, original_degree, low_bound, up_bound):
            deg = input_degree + original_degree
            if not isinstance(up_bound, type(None)):
                deg = min(deg, up_bound)
            if not isinstance(low_bound, type(None)):
                deg = max(deg, low_bound)
            return deg

        if axis not in self.axisBucket:
            raise TypeError("unknown axis for rotation")
        index = self.axisBucket.index(axis)
        if index == 0:
            self.uAngle = limit_rotation(degree, self.uAngle, self.uRange[0], self.uRange[1])
        elif index == 1:
            self.vAngle = limit_rotation(degree, self.vAngle, self.vRange[0], self.vRange[1])
        else:
            self.wAngle = limit_rotation(degree, self.wAngle, self.wRange[0], self.wRange[1])

    def reset(self, mode="all"):
        """
        Reset to default settings
        mode should be "color", "position", "angle", "scale", or "all"
        If mode is "all", then reset everything to default value.

        :param mode: the thing you want to reset
        :type mode: string
        """
        if mode in ["angle", "all"]:
            self.uAngle = self.default_uAngle
            self.vAngle = self.default_vAngle
            self.wAngle = self.default_wAngle
        if mode in ["color", "all"]:
            self.current_color = self.default_color
        if mode in ["position", "all"]:
            self.current_position = self.default_position
        if mode in ["scale", "all"]:
            self.current_scale = copy.deepcopy(self.default_scale)
        if mode in ["rotationAxis", "all"]:
            self.setPreRotation(np.identity(4, dtype=np.double))
            self.setU([1, 0, 0])
            self.setV([0, 1, 0])
            self.setW([0, 0, 1])

    def setRotateExtent(self, axis, minDeg=None, maxDeg=None):
        """
        set rotate extent range for axis rotation

        :param axis: rotation axis. Axis must be uAxis, vAxis, or wAxis
        :param minDeg: rotation's lower limit
        :param maxDeg: rotation's upper limit
        :return: None
        """
        if not axis in self.axisBucket:
            raise TypeError("unknown axis for rotation extent setting")
        # Find out which axis to set
        index = self.axisBucket.index(axis)
        if index == 0:
            r = self.uRange
        elif index == 1:
            r = self.vRange
        else:
            r = self.wRange

        # Update range if any value given
        if not isinstance(minDeg, type(None)):
            iD = minDeg
        else:
            iD = r[0]
        if not isinstance(maxDeg, type(None)):
            aD = maxDeg
        else:
            aD = r[1]
        if iD > aD:
            print("Warning: You shouldn't see this. This means you set minDeg greater than maxDeg. ")
            print("At axis: ", ["u", "v", "w"][index], "   min & max Deg given: ", iD, aD)
            t = iD
            iD = aD
            aD = t
        r[0] = iD
        r[1] = aD

    def setDefaultAngle(self, deg, axis):
        """
        Set default angle for rotation along every axis
        :param axis: rotation axis. Axis must be uAxis, vAxis, or wAxis
        :param deg: the default deg
        :return: None
        """
        if not axis in self.axisBucket:
            raise TypeError("unknown axis for rotation")
        index = self.axisBucket.index(axis)
        if index == 0:
            self.default_uAngle = deg
            self.uAngle = deg
        elif index == 1:
            self.default_vAngle = deg
            self.vAngle = deg
        else:
            self.default_wAngle = deg
            self.wAngle = deg

    def setDefaultColor(self, color):
        """
        Default color for this component
        :param color: color for this component
        :type color: ColorType
        :return: None
        """
        if not isinstance(color, ColorType):
            raise TypeError("color should have type ColorType")
        self.default_color = color.copy()
        self.current_color = copy.deepcopy(self.default_color)

    def setDefaultPosition(self, pos):
        """
        Set default relative translation from parent
        :param pos: default relative translation from parent to this component
        :type pos: Point
        :return:
        """
        if not isinstance(pos, Point):
            raise TypeError("pos should have type Point")
        self.default_position = pos.copy()
        self.current_position = copy.deepcopy(self.default_position)

    def setDefaultScale(self, scale):
        """
        Set default scaling along three axes
        :param scale: default scaling along three axes
        :return: None
        """
        if not isinstance(scale, list) and not isinstance(scale, tuple):
            raise TypeError("default scale should be list or tuple")
        if len(scale) != 3:
            raise TypeError("default scale should consists of scaling on 3 axis")
        self.default_scale = copy.deepcopy(scale)
        self.current_scale = copy.deepcopy(self.default_scale)

    def setCurrentPosition(self, pos):
        """
        Set relative translation from parent
        :param pos: relative translation from parent to this component
        :type pos: Point
        :return:
        """
        if not isinstance(pos, Point):
            raise TypeError("pos should have type Point")
        self.current_position = pos.copy()

    def setCurrentColor(self, color):
        """
        color for this component
        :param color: color for this component
        :type color: ColorType
        :return: None
        """
        if not isinstance(color, ColorType):
            raise TypeError("color should have type ColorType")
        self.current_color = color.copy()

    def setCurrentScale(self, scale):
        """
        Set scaling along three axes
        :param scale: scaling along three axes
        :return: None
        """
        if not isinstance(scale, list) and not isinstance(scale, tuple):
            raise TypeError("current scale should be list or tuple")
        if len(scale) != 3:
            raise TypeError("current scale should consists of scaling on 3 axis")
        self.current_scale = copy.deepcopy(scale)

    def setPreRotation(self, rotation_matrix=None):
        """
        If you want the component to start with a different facing direction before all the following transformation,
        then set a pre-rotation matrix

        :param rotation_matrix: a 4x4 homogenuous transformation matrix
        :type rotation_matrix: numpy.ndarray
        """
        if isinstance(rotation_matrix, np.ndarray):
            self.pre_rotation_matrix = rotation_matrix

    def u(self):
        return self.uAxis.copy()

    def v(self):
        return self.vAxis.copy()

    def w(self):
        return self.wAxis.copy()

    def setU(self, u):
        if len(u) != len(self.uAxis):
            raise TypeError("axis should have the same size as the current one")
        for i in range(len(u)):
            self.uAxis[i] = u[i]

    def setV(self, v):
        if len(v) != len(self.vAxis):
            raise TypeError("axis should have the same size as the current one")
        for i in range(len(v)):
            self.vAxis[i] = v[i]

    def setW(self, w):
        if len(w) != len(self.wAxis):
            raise TypeError("axis should have the same size as the current one")
        for i in range(len(w)):
            self.wAxis[i] = w[i]
