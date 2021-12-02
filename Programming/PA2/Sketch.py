'''
Name:                       Yumiao Zhou
the class:                  CS680 
the assignment number:      PA2
due date:                   Oct.12,2021

Import a robot as the required creature. 
    A robot who has a head, two arms, two legs and two rocket propellers on the back
Set up the required keyboard events(unrelated to the old control system).
    ",<" and ".>" switch current component
    "a" and "d" switch selected axis
    "w" and "s" rotate 
Add 5 test cases.
    use "tT" to cycle through them
'''

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
from wx.core import Display
from ModelPropeller import ModelPropeller
from ModelRobot import ModelRobot

from Point import Point
import ColorType as CT
from ColorType import ORANGE, ColorType
from Quaternion import Quaternion
from Component import Component
from CanvasBase import CanvasBase
from ModelAxes import ModelAxes

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
        import OpenGL.GLUT as glut  # this fails on OS X 11.x
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
        import OpenGL.GLUT as glut
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
    components = []
    select_obj_index = -1  # index in components
    select_axis_index = -1  # index of select axis
    select_color = [ColorType(1, 0, 0), ColorType(0, 1, 0), ColorType(0, 0, 1), ColorType(1,1,1)]
    
    #Slots of New Control System
    curr_component_index = -1
    curr_axis_index = 3
    selected_component = {}
    test_case_index = 0


    def __init__(self, parent):
        """
        Init everything. You should set your model here.
        """
        super(Sketch, self).__init__(parent)
        # prepare OpenGL context
        self.context = glcanvas.GLContext(self)
        # Initialize Parameters
        self.last_mouse_leftPosition = [0, 0]
        

        ##### TODO 3: Import Your Creature
        # You should instance your creature class here, and add it as self.topLevelrtomponent's Child

        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural way
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.

        # coordinate system with x, y, z axies
        # m1 = ModelAxes(self, Point((-1, -1, -1)))  
        # self.topLevelComponent.addChild(m1)
        # self.components = m1.components
        
        # import my model
        my_model = ModelRobot(self,Point((0,0.5,0)),scale=(0.2,0.2,0.2))
        self.topLevelComponent.addChild(my_model)
    
        self.model = my_model
        self.components = my_model.components    

        # Test Cases
        self.test_case_list = [self.testCase1,self.testCase2,self.testCase3,self.testCase4,self.testCase5]


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
        ##### BONUS 2 (TODO 6 for CS680 student): Finishing touch - eyes!
        # Requirements:
        #   1. Add eyes to the creature model, for each it consists of an eyeball and pupil.
        #   2. Make eyes automatically follow the mouse position by rotating the eyeball.
        #   3. (extra credits) Use quaternion to implement the eyeball rotation

        # Approximate positions of eyes and their distance to the screen
        right_eye_position = (self.size[0] * 0.4793388429752066,self.size[1] * 0.8806941431670282)
        left_eye_position = (self.size[0] * 0.5165289256198347,self.size[1] * 0.8806941431670282)
        distance_to_screen = self.size[1] / 2

        # right eye
        dx = x - right_eye_position[0]
        dy = y - right_eye_position[1]
        x_degree = math.atan(dy/distance_to_screen) / math.pi * 180
        y_degree = math.atan(dx/distance_to_screen) / math.pi * 180
        self.model.head.right_eye.setCurrentAngle(-x_degree,self.model.head.right_eye.uAxis)
        self.model.head.right_eye.setCurrentAngle(y_degree,self.model.head.right_eye.wAxis)

        # left eye
        dx = x - left_eye_position[0]
        dy = y - left_eye_position[1]
        x_degree = math.atan(dy/distance_to_screen) / math.pi * 180
        y_degree = math.atan(dx/distance_to_screen) / math.pi * 180
        self.model.head.left_eye.setCurrentAngle(-x_degree,self.model.head.left_eye.uAxis)
        self.model.head.left_eye.setCurrentAngle(y_degree,self.model.head.left_eye.wAxis)

        self.update()
        

    def Interrupt_Keyboard(self, keycode):
        """
        Keyboard interrupt bindings

        :param keycode: wxpython keyboard event's keycode
        :return: None
        """
        ##### TODO 5: Define creature poses and set interface to iterate through them
        # Requirements:
        #   1. Set 5 different poses of the creature.
        #   2. Add a keyboard interface "T" to cycle through the poses.
        #   3. Add multi-select feature to the interface, so you can change multiple joints at the same time. 

        if keycode in [wx.WXK_RETURN]:
            # enter component editing mode
            if len(self.components) > self.select_obj_index >= 0:
                self.components[self.select_obj_index].reset("color")

            self.select_axis_index = 0
            if len(self.components) > 0:
                if self.select_obj_index < 0:
                    self.select_obj_index = 0
                else:
                    self.select_obj_index = (self.select_obj_index + 1) % len(self.components)

            if len(self.components) > self.select_obj_index >= 0:
                self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_LEFT]:
            # Last rotation axis of this component
            self.select_axis_index = (self.select_axis_index - 1) % 3
            if len(self.components) > self.select_obj_index >= 0:
                self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_RIGHT]:
            # Next rotation axis of this component
            self.select_axis_index = (self.select_axis_index + 1) % 3
            if len(self.components) > self.select_obj_index >= 0:
                self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_UP]:
            # Increase rotation angle
            self.Interrupt_Scroll(1)
            self.update()
        if keycode in [wx.WXK_DOWN]:
            # Decrease rotation angle
            self.Interrupt_Scroll(-1)
            self.update()
        if keycode in [wx.WXK_ESCAPE]:
            # exit component editing mode
            if len(self.components) > self.select_obj_index >= 0:
                self.components[self.select_obj_index].reset("color")
            self.select_obj_index = -1
            self.select_axis_index = -1
            self.update()
        if chr(keycode) in "r":
            # reset viewing angle only
            self.viewing_quaternion = Quaternion()
        if chr(keycode) in "R":
            # reset everything
            for c in self.components:
                c.reset()
            self.viewing_quaternion = Quaternion()
            self.select_obj_index = 0
            self.select_axis_index = 0
            self.update()

        # New Control System

        # Choose the previous component
        if chr(keycode) in ",<":
            # Restore the color
            if len(self.components) > self.curr_component_index >= 0:
                if self.curr_component_index not in self.selected_component.keys() or self.selected_component[self.curr_component_index] == 3:
                    self.components[self.curr_component_index].reset("color")
                else:
                    self.components[self.curr_component_index].setCurrentColor(self.select_color[self.selected_component[self.curr_component_index]])

            self.curr_axis_index = 3

            # Move to the previous component
            if len(self.components) > 0:
                if self.curr_component_index < 0:
                    self.curr_component_index = len(self.components) - 1
                else:
                    self.curr_component_index = (self.curr_component_index - 1) % len(self.components)

            # Set the color to highlight it 
            if len(self.components) > self.curr_component_index >= 0:
                self.components[self.curr_component_index].setCurrentColor(self.select_color[3])
            self.update()

        # Choose the next component
        if chr(keycode) in ".>":
            # Restore the color
            if len(self.components) > self.curr_component_index >= 0:
                if self.curr_component_index not in self.selected_component.keys() or self.selected_component[self.curr_component_index] == 3:
                    self.components[self.curr_component_index].reset("color")
                else:
                    self.components[self.curr_component_index].setCurrentColor(self.select_color[self.selected_component[self.curr_component_index]])

            self.curr_axis_index = 3
            
            # Move to the next component
            if len(self.components) > 0:
                if self.curr_component_index < 0:
                    self.curr_component_index = 0
                else:
                    self.curr_component_index = (self.curr_component_index + 1) % len(self.components)

            # Set the color to highlight it 
            if len(self.components) > self.curr_component_index >= 0:
                self.components[self.curr_component_index].setCurrentColor(self.select_color[3])
            self.update()

        # Choose the previous axis
        if chr(keycode) in "aA":
            self.curr_axis_index = (self.curr_axis_index - 1) % 4
            if len(self.components) > self.curr_component_index >= 0:
                self.components[self.curr_component_index].setCurrentColor(self.select_color[self.curr_axis_index])
                self.selected_component[self.curr_component_index] = self.curr_axis_index
            self.update()

        # Choose the next axis
        if chr(keycode) in "dD":
            self.curr_axis_index = (self.curr_axis_index + 1) % 4
            if len(self.components) > self.curr_component_index >= 0:
                self.components[self.curr_component_index].setCurrentColor(self.select_color[self.curr_axis_index])
                self.selected_component[self.curr_component_index] = self.curr_axis_index
            self.update()

        # Rotate positively
        if chr(keycode) in "wW":
            for index in self.selected_component.keys():
                axis_index = self.selected_component[index]
                if axis_index != 3:
                    self.components[index].rotate(5,self.components[index].axisBucket[axis_index])
            self.update()

        # Rotate negatively
        if chr(keycode) in "sS":
            for index in self.selected_component.keys():
                axis_index = self.selected_component[index]
                if axis_index != 3:
                    self.components[index].rotate(-5,self.components[index].axisBucket[axis_index])
            self.update()

        # Cycle throught the cases
        if chr(keycode) in "tT":
            self.reset()
            if len(self.test_case_list) != 0:
                self.test_case_list[self.test_case_index]()
                self.test_case_index = (self.test_case_index + 1) % len(self.test_case_list)
            

    def reset(self):
        for c in self.components:
                c.reset()
        self.update()

    def testCase1(self):
        self.model.test_case_1()
        self.update()

    def testCase2(self):
        self.model.test_case_2()
        self.update()

    def testCase3(self):
        self.model.test_case_3()
        self.update()

    def testCase4(self):
        self.model.test_case_4()
        self.update()

    def testCase5(self):
        self.model.test_case_5()
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
