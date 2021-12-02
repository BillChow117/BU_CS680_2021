'''
Define our Displayable Tank for vivarium at here.
Created on Oct 26, 2018

:author: micou(Zezhou Sun)
:version: 2021.1.1
'''
import os
import time
import numpy as np

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
try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError

from Buff import Buff
from Displayable import Displayable


class DisplayableTank(Displayable):
    """
    origin locate at the center of tank.(Not at bottom left point)
    """

    callListHandle = 0  # long int. override the one in Displayable
    qd = None  # Quadric
    textureID = 0  # long int. This is a textureID id in openGL.
    textureOn = False
    textureImg = None
    textureImgSize = None
    w = 0
    d = 0
    h = 0

    def __init__(self, parent, w, d, h):
        super().__init__(parent)
        self.w = w
        self.d = d
        self.h = h
        parent.context.SetCurrent(parent)
        self.textureID = gl.glGenTextures(1)
        self.readTexture()
        self.textureOn = self.textureID != 0

    def readTexture(self):
        """
        Used to update texture
        """
        # we generate default texture, takes about 20ms in constructing
        self.textureImgSize = (128, int(128 * self.d / self.w))
        image = Buff(*self.textureImgSize)
        block_size = 16
        for i in range(self.textureImgSize[0]):
            for j in range(self.textureImgSize[1]):
                if ((int(i / block_size) % 2 == 0 and int(j / block_size) % 2 == 0) or
                        (int(i / block_size) % 2 == 1 and int(j / block_size) % 2) == 1):
                    image.setPixel(i, j, 255, 255, 255)
        self.textureImg = image.getBytes()

    def setTexture(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureID)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE)
        #         gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_DECAL) # Tex1ture only mode
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, self.textureImgSize[0], self.textureImgSize[1],
                        0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, self.textureImg)

    def draw(self):
        if self.textureOn:
            self.setTexture()  # This is required every time you need to redraw objects
        gl.glCallList(self.callListHandle)

    def initialize(self):
        """
        Create a wired cube
        """
        self.callListHandle = gl.glGenLists(1)
        self.qd = glu.gluNewQuadric()

        gl.glNewList(self.callListHandle, gl.GL_COMPILE)
        # Start to draw tank edges
        gl.glColor3f(0.65, 0.0, 0.45)
        gl.glPushMatrix()
        gl.glLineWidth(1)
        gl.glBegin(gl.GL_LINE_STRIP)
        gl.glVertex3f(self.w / 2, self.h / 2, self.d / 2)
        gl.glVertex3f(-self.w / 2, self.h / 2, self.d / 2)
        gl.glVertex3f(-self.w / 2, -self.h / 2, self.d / 2)
        gl.glVertex3f(self.w / 2, -self.h / 2, self.d / 2)
        gl.glVertex3f(self.w / 2, self.h / 2, self.d / 2)
        gl.glVertex3f(self.w / 2, self.h / 2, -self.d / 2)
        gl.glVertex3f(-self.w / 2, self.h / 2, -self.d / 2)
        gl.glVertex3f(-self.w / 2, -self.h / 2, -self.d / 2)
        gl.glVertex3f(self.w / 2, -self.h / 2, -self.d / 2)
        gl.glVertex3f(self.w / 2, self.h / 2, -self.d / 2)
        gl.glEnd()
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(-self.w / 2, -self.h / 2, self.d / 2)
        gl.glVertex3f(-self.w / 2, -self.h / 2, -self.d / 2)
        gl.glVertex3f(-self.w / 2, self.h / 2, self.d / 2)
        gl.glVertex3f(-self.w / 2, self.h / 2, -self.d / 2)
        gl.glVertex3f(self.w / 2, -self.h / 2, self.d / 2)
        gl.glVertex3f(self.w / 2, -self.h / 2, -self.d / 2)
        gl.glEnd()
        gl.glPopMatrix()
        # Start to draw bottom, and only apply texture to bottom
        gl.glColor3f(1, 1, 1)
        if self.textureOn:
            glu.gluQuadricDrawStyle(self.qd, glu.GLU_FILL)
            glu.gluQuadricTexture(self.qd, True)
            glu.gluQuadricNormals(self.qd, glu.GLU_SMOOTH)
            gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glPushMatrix()
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2f(1.0, 1.0)
        gl.glVertex3f(self.w / 2, -self.h / 2, self.d / 2)
        gl.glTexCoord2f(1.0, 0.0)
        gl.glVertex3f(self.w / 2, -self.h / 2, -self.d / 2)
        gl.glTexCoord2f(0.0, 0.0)
        gl.glVertex3f(-self.w / 2, -self.h / 2, -self.d / 2)
        gl.glTexCoord2f(0.0, 1.0)
        gl.glVertex3f(-self.w / 2, -self.h / 2, self.d / 2)
        gl.glEnd()
        if self.textureOn:
            gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glPopMatrix()
        gl.glEndList()

        glu.gluDeleteQuadric(self.qd)
