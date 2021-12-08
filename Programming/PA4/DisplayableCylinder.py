"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA4
due date:                   Dec.07,2021

switch to render with EBO

EBO:
Column | 0:3                | 3:6           | 6:9          |
Stores | Vertex coordinates | Vertex normal | Vertex Color |
"""

"""
Define displayable cube here. Current version only use VBO
First version in 10/20/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import math

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


class DisplayableCylinder(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    radius = None
    length = None
    stacks = None
    slices = None
    color = None

    def __init__(self, shaderProg, radius=1, length= 4, stacks=18, slices=36, color=ColorType.BLUE):
        super().__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(radius, length, stacks, slices, color)

    def generate(self, radius=1, length= 4, stacks=18, slices=36, color=None):
        self.radius = radius
        self.length = length
        self.stacks = stacks
        self.slices = slices
        self.color = color
        
        # two center points of each caps + two points for each slices
        # self.vtxCoord[0,:,:] for upper layer, self.vtxCoord[1,:,:] for lower layer
        self.vtxCoord = np.zeros([2,1 + slices, 3])
        self.vtxCoord[0,-1,:] = [0,0,self.length / 2] 
        self.vtxCoord[1,-1,:] = [0,0,-self.length / 2]    
        for i in range(slices):
            theta = i / (slices) * 2 * math.pi
            # vertex on top edge
            self.vtxCoord[0,i,:] = [self.radius * math.cos(theta),
                                    self.radius * math.sin(theta),
                                    self.length / 2]
            # vertex on bottom edge
            self.vtxCoord[1,i,:] = [self.radius * math.cos(theta),
                                    self.radius * math.sin(theta),
                                    -self.length / 2]

        # there are 4 triangles in each slice, 2 in top and bottom, 2 in side grid, 12 points in total
        self.vertices = np.zeros([12 * slices,11])
        for i in range(slices):
            next_i = (i+1)%slices
            # triangle on top cap
            self.vertices[12 * i + 0, 0:3] = self.vtxCoord[0,-1,:]
            self.vertices[12 * i + 1, 0:3] = self.vtxCoord[0,i,:]
            self.vertices[12 * i + 2, 0:3] = self.vtxCoord[0,next_i,:]
            
            self.vertices[12 * i + 0, 3:6] = [0,0,1]
            self.vertices[12 * i + 1, 3:6] = [0,0,1]
            self.vertices[12 * i + 2, 3:6] = [0,0,1]
            
            # triangles on side grid
            self.vertices[12 * i + 3, 0:3] = self.vtxCoord[0,i,:]
            self.vertices[12 * i + 4, 0:3] = self.vtxCoord[1,i,:]
            self.vertices[12 * i + 5, 0:3] = self.vtxCoord[1,next_i,:]
            
            self.vertices[12 * i + 3, 3:5] = self.vtxCoord[0,i,:2]
            self.vertices[12 * i + 4, 3:5] = self.vtxCoord[1,i,:2]
            self.vertices[12 * i + 5, 3:5] = self.vtxCoord[1,next_i,:2]
            
            self.vertices[12 * i + 6, 0:3] = self.vtxCoord[0,i,:]
            self.vertices[12 * i + 7, 0:3] = self.vtxCoord[1,next_i,:]
            self.vertices[12 * i + 8, 0:3] = self.vtxCoord[0,next_i,:]
            
            self.vertices[12 * i + 6, 3:5] = self.vtxCoord[0,i,:2]
            self.vertices[12 * i + 7, 3:5] = self.vtxCoord[1,next_i,:2]
            self.vertices[12 * i + 8, 3:5] = self.vtxCoord[0,next_i,:2]
            
            # triangle on bottom cap
            self.vertices[12 * i + 9, 0:3] = self.vtxCoord[1,-1,:]
            self.vertices[12 * i + 10, 0:3] = self.vtxCoord[1,next_i,:]
            self.vertices[12 * i + 11, 0:3] = self.vtxCoord[1,i,:]
            
            self.vertices[12 * i + 9, 3:6] = [0,0,-1]
            self.vertices[12 * i + 10, 3:6] = [0,0,-1]
            self.vertices[12 * i + 11, 3:6] = [0,0,-1]

            
        self.indices = np.array(range(4*3*slices)).reshape([4*slices,3])

        self.vertices[:,6:9] = [*color]


        

    def draw(self):
        self.vao.bind()
        # TODO 1.1 is at here, switch from vbo to ebo
        #self.vbo.draw()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems that don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 11)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"),
                                  stride=11, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"),
                                  stride=11, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"),
                                  stride=11, offset=6, attribSize=3)
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()

