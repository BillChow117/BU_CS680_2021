"""
Set up our display pipeline. WxPython is used to solve system compatibility problems. It is mainly focusing on
creating a display window with a canvas. We will let OpenGL draw on it. All these things have been wrapped up,
and the main class should inherit this class. Created on 20180923

:author: micou(Zezhou Sun)
:version: 2021.1.3
"""
try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")

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

import math
import random
import numpy as np

from Point import Point
from Component import Component
from ColorType import ColorType
from Quaternion import Quaternion

############################### System Checking ################################

WX_MINIMUM_REQUIRED = "3.0.0"
OPENGL_MINIMUM_REQUIRED = "3.1.0"

# Package version checking
if wx.__version__ < WX_MINIMUM_REQUIRED:
    # Not fully tested yet. But version 3.0.0+ should work based on changelog
    raise ImportError("wxPython minimum required " + WX_MINIMUM_REQUIRED)
if OpenGL.__version__ < OPENGL_MINIMUM_REQUIRED:
    # Not fully tested yet.
    raise ImportError("PyOpenGL minimum required " + OPENGL_MINIMUM_REQUIRED)


############################ End of System Checking #############################

########## TO DO LIST
# 1. Resize canvas and debug the onsize problem

class CanvasBase(glcanvas.GLCanvas):
    """
    All functions work on interruptions and events start with capital letter
    functions for public use start with lower case letter
    functions for local use (accessible from outside) start with _(single underscore)
    functions for private use (not accessible outside) start with __ (double underscore)
    """
    size = None
    context = None
    stateChanged = False
    topLevelComponent = None
    init = False
    viewing_quaternion = None

    animator = True  # Switch for animation. If this on, frame will update according to fps settings
    timer = None  # wxpython timer. Used to control fps
    fps = 60  # animation frame per second, -1 to disable animation (update will only triggered by mouse & keyboard event).
    animation_update = False  # bool. Only update when frame refreshes by fps

    def __init__(self, parent):
        # Initialize parent class
        attrib = glcanvas.GLAttributes()
        # Defaults() is required. Otherwise MacOS will get blank screen,
        # For the depth size, macOS support <= 24, Windows support 16-32, Linux requires >= 24
        attrib.Defaults().Depth(24).EndList()
        super(CanvasBase, self).__init__(parent, attrib)
        # Initialize public variables
        self.stateChanged = False
        self.init = False
        self.size = (0, 0)
        self.topLevelComponent = Component(Point((0, 0, 0)))
        self.viewing_quaternion = Quaternion()
        self.timer = wx.Timer(self, 1)  # TIMER_ID set to 1

        # Bind event to functions
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeft)
        self.Bind(wx.EVT_RIGHT_UP, self.OnMouseRight)
        self.Bind(wx.EVT_CHAR, self.OnKeyDown)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        if self.fps > 0:
            self.timer.Start(1000 / self.fps, oneShot=wx.TIMER_CONTINUOUS)

    def OnResize(self, event):
        """
        Called when resize of window happen, this will run before OnPaint in first running
        """
        self.context = glcanvas.GLContext(self)
        self.size = self.GetClientSize()
        self.size[1] = max(1, self.size[1])  # avoid divided by 0
        self.SetCurrent(self.context)

        # Set up camera
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glViewport(0, 0, self.size[0], self.size[1])
        glu.gluPerspective(25, float(self.size[0]) / self.size[1], 0.1, 100)
        glu.gluLookAt(0, 0, 12, 0, 0, 0, 0, 1, 0)  # Camera at (0, 0, 24), look at (0, 0, 0), up vector (0, 1, 0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

        # Update screen and display
        self.init = False
        self.Refresh(eraseBackground=True)

    def OnPaint(self, event=None):
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        if self.stateChanged:
            self.__modelChanged()
            self.stateChanged = False
        self.OnDraw()

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

        # Swap Buffer to display canvas
        self.SwapBuffers()

    def InitGL(self):
        """
        Only used when canvas property changed. Will reset lighting
        """
        self.SetCurrent(self.context)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        self.size = self.GetClientSize()

        # Initialize all components and draw them
        self.topLevelComponent.initialize()
        self.topLevelComponent.update()

        # Set up display environment
        gl.glPolygonMode(gl.GL_FRONT, gl.GL_FILL)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT, gl.GL_AMBIENT_AND_DIFFUSE)

        # clear background on canvas.
        gl.glClearColor(0, 0, 0, 0)
        gl.glShadeModel(gl.GL_SMOOTH)

        # Enable depth comparison and norm vector normalization
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_NORMALIZE)

        # Enable lighting, but light source not defined yet. Defined at OnDraw
        gl.glEnable(gl.GL_LIGHTING)

    def OnTimer(self, event):
        if self.animator:
            self.animation_update = True
            self.Refresh(True)

    def OnDestroy(self, event):
        print("Destroy Window")

    def OnMouseMotion(self, event):
        if event.LeftIsDown():
            # If this is a dragging event with left button down
            self.Interrupt_MouseLeftDragging(event.GetX(), self.size.height - event.GetY())
            self.Refresh(True)
        elif event.RightIsDown():
            # If this is a dragging event with right button down
            self.Interrupt_MouseRightDragging(event.GetX(), self.size.height - event.GetY())
            self.Refresh(True)
        else:
            # Normal Mouse Moving, if you changed model in here, don't forget to refresh it. 
            self.Interrupt_MouseMoving(event.GetX(), self.size.height - event.GetY())

    # Definition for interface
    def OnMouseLeft(self, event):
        x = event.GetX()
        y = event.GetY()
        self.Interrupt_MouseL(x, self.size.height - y)
        self.Refresh(True)

    def OnMouseRight(self, event):
        x = event.GetX()
        y = event.GetY()
        self.Interrupt_MouseR(x, self.size.height - y)
        self.Refresh(True)

    def OnKeyDown(self, event):
        #         keyunicode = event.GetUnicodeKey() # This one only have limited key code
        keycode = event.GetKeyCode()
        self.Interrupt_Keyboard(keycode)
        self.Refresh(True)

    def __modelChanged(self):
        """
        Only used when model updated, this is only used when stateChanged
        """
        self.topLevelComponent.update()

    def modelUpdate(self):
        """
        Call this method every time the model has changed
        """
        self.stateChanged = True

    def Interrupt_MouseL(self, x, y):
        pass  # Fully Override please

    def Interrupt_MouseR(self, x, y):
        pass  # Fully Override please

    def Interrupt_Keyboard(self, keycode):
        pass  # Fully Override please

    def Interrupt_MouseLeftDragging(self, x, y):
        pass  # Fully Override please

    def Interrupt_MouseRightDragging(self, x, y):
        pass  # Fully Override please

    def Interrupt_MouseMoving(self, x, y):
        pass  # Fully Override please


if __name__ == "__main__":
    print("Not in main!")

    app = wx.App(False)
    # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame, here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
    # Resize disabled in this one
    frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
    canvas = CanvasBase(frame)

    frame.Show()
    app.MainLoop()
