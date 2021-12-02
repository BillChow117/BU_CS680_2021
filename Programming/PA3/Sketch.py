"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA3
due date:                   Nov.09,2021

Add a keyboard event "fF" to add food particle to the tank.
"""

'''
This is the main entry of your program. Almost all things you need to implement are in this file.
The main class Sketch inherits from CanvasBase. For the parts you need to implement, they are all marked with TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun)
:version: 2021.2.1
'''
import os
import wx
import time
import math
import random
import numpy as np

from Point import Point
import ColorType as CT
from ColorType import ColorType
from Quaternion import Quaternion
from CanvasBase import CanvasBase
from Vivarium import Vivarium

try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")
try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError
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


class Sketch(CanvasBase):
    """
    Drawing methods and interrupt methods will be implemented in this class.

    Variable Instruction:
        * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will print more details and do some type checking, which might be helpful in debugging


    Method Instruction:


    Here are the list of functions you need to override:
        * Interrupt_MouseL: Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
        * Interrupt_MouseLeftDragging: Used to deal with mouse dragging interruption.
        * Interrupt_Keyboard: Used to deal with keyboard press interruption. Use this to add new keys or new methods

    Here are some public variables in parent class you might need:


    """
    context = None

    debug = 1

    last_mouse_leftPosition = None
    components = None
    select_obj_index = -1  # index in components
    select_axis_index = -1  # index of select axis
    select_color = [ColorType(1, 0, 0), ColorType(0, 1, 0), ColorType(0, 0, 1)]

    def __init__(self, parent):
        super(Sketch, self).__init__(parent)
        # Initialize Parameters
        self.last_mouse_leftPosition = [0, 0]
        # add components to top level
        self.context = glcanvas.GLContext(self)

        self.vivarium = Vivarium(self)  # all things at here
        self.topLevelComponent.addChild(self.vivarium)
        self.components = self.vivarium.components

    def OnDraw(self):
        # Set up light source
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, [1, 1, 1, 0], 0)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, [0.25, 0.25, 0.25, 1], 0)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, [1, 1, 1, 1], 0)
        gl.glEnable(gl.GL_LIGHT0)

        self.SetCurrent(self.context)
        # clear color buffer and depth buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # set to model view

        gl.glMatrixMode(gl.GL_MODELVIEW)
        # Replace current matrix with identity matrix
        gl.glLoadIdentity()
        gl.glMultMatrixf(self.viewing_quaternion.toMatrix(), 0)
        self.topLevelComponent.draw()

        if self.animation_update:
            # when it is time for animation update, self.animation_update(defined in CanvasBase) will be set to True
            self.vivarium.animationUpdate()
            self.animation_update = False

        # Swap Buffer to display canvas
        self.SwapBuffers()

    def Interrupt_Scroll(self, wheelRotation):
        """
        When mouse wheel rotating detected, do following things

        :param wheelRotation: mouse wheel changes, normally +120 or -120
        :return: None
        """
        wheelChange = wheelRotation / abs(wheelRotation)  # normalize wheel change
        if len(self.components) > self.select_obj_index >= 0:
            self.components[self.select_obj_index].rotate(wheelChange * 5,
                                                          self.components[self.select_obj_index].
                                                          axisBucket[self.select_axis_index])
        self.update()

    def Interrupt_MouseL(self, x, y):
        """
        When mouse click detected, store current position in last_mouse_leftPosition

        :param x: Mouse click's x coordinate
        :type x: int
        :param y: Mouse click's y coordinate
        :type y: int
        :return: None
        """
        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def Interrupt_MouseLeftDragging(self, x, y):
        """
        When mouse drag motion detected, interrupt with new mouse position

        :param x: Mouse drag new position's x coordinate
        :type x: int
        :param y: Mouse drag new position's x coordinate
        :type y: int
        :return: None
        """
        # Change viewing angle when dragging happened
        dx = x - self.last_mouse_leftPosition[0]
        dy = y - self.last_mouse_leftPosition[1]
        mag = math.sqrt(dx * dx + dy * dy)
        axis = (dy / mag, -dx / mag, 0) if mag != 0 else (1, 0, 0)
        viewing_delta = 3.14159265358 / 180
        s = math.sin(0.5 * viewing_delta)
        c = math.cos(0.5 * viewing_delta)
        q = Quaternion(c, s * axis[0], s * axis[1], s * axis[2])
        self.viewing_quaternion = q.multiply(self.viewing_quaternion)
        self.viewing_quaternion.normalize()  # to correct round-off error caused by cos/sin
        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def update(self):
        """
        Update current canvas
        :return: None
        """
        self.modelUpdate()

    def Interrupt_MouseMoving(self, x, y):
        pass

    def Interrupt_Keyboard(self, keycode):
        """
        Keyboard interrupt bindings

        :param keycode: wxpython keyboard event's keycode
        :return: None
        """
        if chr(keycode) in "rR":
            # reset viewing angle only
            self.viewing_quaternion = Quaternion()
            self.update()
        
        if chr(keycode) in "fF":
            # add food in the tank
            self.vivarium.addfood()
            self.update()


if __name__ == "__main__":
    print("This is the main entry! ")
    app = wx.App(False)
    # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame, here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
    # Resize disabled in this one
    frame = wx.Frame(None, size=(500, 500), title="Test",
                     style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)  # Disable Resize: ^ wx.RESIZE_BORDER
    canvas = Sketch(frame)

    frame.Show()
    app.MainLoop()
