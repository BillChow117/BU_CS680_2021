"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA4
due date:                   Dec.07,2021

Switched to renderring with EBO
Extended EBO to support texture mapping, normal mapping

EBO:
Column | 0:3                | 3:6           | 6:9          | 9:11                       | 11:14                 | 14:17                 |
Stores | Vertex coordinates | Vertex normal | Vertex Color | Vertex texture Coordinates | du for normal mapping | dv for normal mapping |
"""

"""
Define displayable cube here. Current version only use VBO
First version in 10/20/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
import numpy as np
import ColorType

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


class DisplayableCube(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    length = None
    width = None
    height = None
    color = None

    def __init__(self, shaderProg, length=1, width=1, height=1, color=ColorType.BLUE):
        super(DisplayableCube, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(length, width, height, color)

    def generate(self, length=1, width=1, height=1, color=None):
        self.length = length
        self.width = width
        self.height = height
        self.color = color
        
        self.vertices = np.zeros([36, 17])
        
        vl = np.array([
            # back face
            -length/2, -width/2, -height/2, 0, 0, -1, *color,1,0,-1,0,0,0,1,0,
            -length/2, width/2, -height/2, 0, 0, -1, *color,1,1,-1,0,0,0,1,0,
            length/2, width/2, -height/2, 0, 0, -1, *color,0,0,-1,0,0,0,1,0,
            -length / 2, -width / 2, -height / 2, 0, 0, -1, *color,1,0,-1,0,0,0,1,0,
            length / 2, width / 2, -height / 2, 0, 0, -1, *color,0,1,-1,0,0,0,1,0,
            length/2, -width/2, -height/2, 0, 0, -1, *color,0,0,-1,0,0,0,1,0,
            # front face
            -length/2, -width/2, height/2, 0, 0, 1, *color,0,0,1,0,0,0,1,0,
            length/2, -width/2, height/2, 0, 0, 1, *color,1,0,1,0,0,0,1,0,
            length/2, width/2, height/2, 0, 0, 1, *color,1,1,1,0,0,0,1,0,
            -length / 2, -width / 2, height / 2, 0, 0, 1, *color,0,0,1,0,0,0,1,0,
            length / 2, width / 2, height / 2, 0, 0, 1, *color,1,1,1,0,0,0,1,0,
            -length/2, width/2, height/2, 0, 0, 1, *color,0,1,1,0,0,0,1,0,
            # left face
            -length/2, -width/2, -height/2, -1, 0, 0, *color,0,0,0,0,1,0,1,0,
            -length/2, -width/2, height/2, -1, 0, 0, *color,1,0,0,0,1,0,1,0,
            -length/2, width/2, height/2, -1, 0, 0, *color,1,1,0,0,1,0,1,0,
            -length / 2, -width / 2, -height / 2, -1, 0, 0, *color,0,0,0,0,1,0,1,0,
            -length / 2, width / 2, height / 2, -1, 0, 0, *color,1,1,0,0,1,0,1,0,
            -length/2, width/2, -height/2, -1, 0, 0, *color,0,1,0,0,1,0,1,0,
            # right face
            length/2, -width/2, height/2, 1, 0, 0, *color,0,0,0,0,-1,0,1,0,
            length/2, -width/2, -height/2, 1, 0, 0, *color,1,0,0,0,-1,0,1,0,
            length/2, width/2, -height/2, 1, 0, 0, *color,1,1,0,0,-1,0,1,0,
            length / 2, -width / 2, height / 2, 1, 0, 0, *color,0,0,0,0,-1,0,1,0,
            length / 2, width / 2, -height / 2, 1, 0, 0, *color,1,1,0,0,-1,0,1,0,
            length/2, width/2, height/2, 1, 0, 0, *color,0,1,0,0,-1,0,1,0,
            # top face
            -length/2, width/2, height/2, 0, 1, 0, *color,0,0,1,0,0,0,0,-1,
            length/2, width/2, height/2, 0, 1, 0, *color,1,0,1,0,0,0,0,-1,
            length/2, width/2, -height/2, 0, 1, 0, *color,1,1,1,0,0,0,0,-1,
            -length / 2, width / 2, height / 2, 0, 1, 0, *color,0,0,1,0,0,0,0,-1,
            length / 2, width / 2, -height / 2, 0, 1, 0, *color,1,1,1,0,0,0,0,-1,
            -length/2, width/2, -height/2, 0, 1, 0, *color,0,1,1,0,0,0,0,-1,
            # bot face
            -length/2, -width/2, -height/2, 0, -1, 0, *color,0,0,1,0,0,0,0,1,
            length/2, -width/2, -height/2, 0, -1, 0, *color,1,0,1,0,0,0,0,1,
            length/2, -width/2, height/2, 0, -1, 0, *color,1,1,1,0,0,0,0,1,
            -length / 2, -width / 2, -height / 2, 0, -1, 0, *color,0,0,1,0,0,0,0,1,
            length / 2, -width / 2, height / 2, 0, -1, 0, *color,1,1,1,0,0,0,0,1,
            -length/2, -width/2, height/2, 0, -1, 0, *color,0,1,1,0,0,0,0,1
        ]).reshape((36, 17))
        
        self.vertices[:,0:17] = vl
        
        self.indices = np.array(range(36)).reshape([12,3])

    def draw(self):
        self.vao.bind()
        # TODO 1.1 is at here, switch from vbo to ebo
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems that don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 17)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"),
                                  stride=17, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"),
                                  stride=17, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"),
                                  stride=17, offset=6, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexTexture"),
                                  stride=17, offset=9, attribSize=2)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexDU"),
                                  stride=17, offset=11, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexDV"),
                                  stride=17, offset=14, attribSize=3)
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()

