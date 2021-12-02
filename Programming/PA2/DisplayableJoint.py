'''
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA2
due date:                   Oct.12,2021

A class to draw a Displayable Joint consisting of two Sphere caps and a round cylinder which grows along z axis at the orgin point of xy plane
'''
import os
import numpy as np
import string

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

try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError

from Displayable import Displayable


class DisplayableJoint(Displayable):

    callListHandle = 0  # long int. override the one in Displayable
    qd = None  # Quadric
    scale = None
    edgeLength = 1
    radius = 1
    height = 1
    _bufferData = None

    def __init__(self, parent, radius = 1, height = 5, scale=None):
        super().__init__(parent)
        parent.context.SetCurrent(parent)
        self.radius = radius
        self.height = height
        if scale is None:
            scale = [1, 1, 1]
        self.scale = scale


    def draw(self):
        gl.glCallList(self.callListHandle)

    def initialize(self):
        self.callListHandle = gl.glGenLists(1)
        self.qd = glu.gluNewQuadric()

        gl.glNewList(self.callListHandle, gl.GL_COMPILE)
        gl.glPushMatrix()

        gl.glScale(*self.scale)

        glu.gluSphere(self.qd,self.radius,36,18)

        glu.gluCylinder(self.qd,self.radius/2,self.radius/2,self.height,36,18)

        gl.glTranslate(0,0,self.height)
        glu.gluSphere(self.qd,self.radius,36,18)


        gl.glPopMatrix()
        gl.glEndList()

