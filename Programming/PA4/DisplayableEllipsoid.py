"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA4
due date:                   Dec.07,2021

Switched to renderring with EBO

EBO:
Column | 0:3                | 3:6           | 6:9          | 9:11                       | 
Stores | Vertex coordinates | Vertex normal | Vertex Color | Vertex texture Coordinates |
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


class DisplayableEllipsoid(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    radius_x = None
    radius_y = None
    radius_z = None
    stacks = None
    slices = None
    color = None

    def __init__(self, shaderProg, radius_x=1, radius_y=2, radius_z=3, stacks=18, slices=36, color=ColorType.BLUE):
        super().__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(radius_x, radius_y, radius_z, stacks, slices, color)

    def generate(self, radius_x=1, radius_y=2, radius_z=3, stacks=18, slices=36, color=None):
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.radius_z = radius_z
        self.stacks = stacks
        self.slices = slices
        self.color = color
        
        # first store all vertices coordinates information in a 3D grid
        self.vtxCoord = np.zeros([stacks, slices, 3])
        for i in range(stacks):
            phi = i / (stacks - 1) * math.pi - math.pi/2
            for j in range(slices):
                theta = j / (slices) * 2 * math.pi - math.pi
                self.vtxCoord[i, j, :] = [
                                            # swap y and z in the equation to make earth looks formal
                                            self.radius_x *  math.cos(phi) * math.cos(theta),
                                            self.radius_y *  math.sin(phi),
                                            self.radius_z *  math.cos(phi) * math.sin(theta)
                                          ]
                
        self.vertices = np.zeros([(stacks) * (slices+1), 11])
        self.vertices[:,6:9] = [*color]

        for i in range(stacks):
            for j in range(slices+1):
                normal_parameter = np.array([2/self.radius_x**2,2/self.radius_y**2,2/self.radius_z**2])
                [x,y,z] = self.vtxCoord[i%stacks,j%slices]
                # vertex coords
                self.vertices[i * (slices+1) + j,0:3] = [x,y,z]
                # vertex normal
                self.vertices[i * (slices+1) + j,3:6] = np.multiply([x,y,z],normal_parameter)
                # vertex texture coords
                self.vertices[i * (slices+1) + j,9:11] = [1-j/slices,i/(stacks-1)]

                    
        self.indices = np.zeros([2 * stacks * (slices+1), 3])
        for i in range(stacks-1):
            for j in range(slices):
                next_i = i+1
                next_j = j+1
                # grid number
                grid_n = i * (slices+1) + j
                # draw two triangles for each grid
                self.indices[2 * grid_n + 0] = [i * (slices+1) + j,i * (slices+1) + next_j, next_i * (slices+1) + next_j]
                self.indices[2 * grid_n + 1] = [i * (slices+1) + j,next_i * (slices+1) + next_j, next_i * (slices+1) + j]
        

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
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexTexture"),
                                  stride=11, offset=9, attribSize=2)
        
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()

