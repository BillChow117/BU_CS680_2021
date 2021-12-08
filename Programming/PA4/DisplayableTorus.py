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
Define Torus here.
First version in 11/01/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
from Point import Point
import numpy as np
import ColorType
import math
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

##### TODO 6/BONUS 6: Texture Mapping
# Requirements:
#   1. Set up each object's vertex texture coordinates(2D) to the self.vertices 9:11 columns
#   (i.e. the last two columns). Tell OpenGL how to interpret these two columns:
#   you need to set up attribPointer in the Displayable object's initialize method.
#   2. Generate texture coordinates for the torus and sphere. Use “./assets/marble.jpg” for the torus and
#   “./assets/earth.jpg” for the sphere as the texture image.
#   There should be no seams in the resulting texture-mapped model.

class DisplayableTorus(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    nsides = 0
    rings = 0
    innerRadius = 0
    outerRadius = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTBLUE):
        super(DisplayableTorus, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(innerRadius, outerRadius, nsides, rings, color)

    def generate(self, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTBLUE):
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.nsides = nsides
        self.rings = rings
        self.color = color
        
        self.vtxCoord = np.zeros([rings, nsides, 9])                
        for i in range(rings):
                phi = i / (rings) * 2 * math.pi
                for j in range(nsides):
                    theta = j / (nsides ) * 2 * math.pi
                    # vertex coords
                    self.vtxCoord[i,j,:3] = [(outerRadius + innerRadius * math.cos(theta)) * math.cos(phi),
                                            (outerRadius + innerRadius * math.cos(theta)) * math.sin(phi),
                                            innerRadius * math.sin(theta)]
                    # du
                    self.vtxCoord[i,j,3:6] = [-(outerRadius + innerRadius * math.cos(theta)) * math.sin(phi),
                                              (outerRadius + innerRadius * math.cos(theta)) * math.cos(phi),
                                            0]
                    # dv
                    self.vtxCoord[i,j,6:9] = [-innerRadius * math.sin(theta) * math.cos(phi),
                                            -innerRadius * math.sin(theta) * math.sin(phi),
                                            innerRadius * math.cos(theta)]

        # we need to pad one more row for both nsides and rings, to assign correct texture coord to them
        self.vertices = np.zeros([(nsides+1) * (rings+1), 17])
        self.vertices[:,6:9] = [*color]

        for i in range(rings+1):
            for j in range(nsides+1):
                [x,y,z,xu,yu,zu,xv,yv,zv] = self.vtxCoord[i%rings,j%nsides]
                # vertex coords
                self.vertices[i * (nsides+1) + j,0:3] = [x,y,z]
                a = 1 - outerRadius / math.sqrt(x**2 + y**2)
                # vertex normal
                self.vertices[i * (nsides+1) + j,3:6] = [a*x,a*y,z]
                # vertex texture coords
                self.vertices[i * (nsides+1) + j,9:11] = [i/rings,j/nsides]
                # du
                self.vertices[i * (nsides+1) + j,11:14] = [xu,yu,zu]
                # dv
                self.vertices[i * (nsides+1) + j,14:17] = [xv,yv,zv]

                    
        self.indices = np.zeros([2 * (nsides+1) * (rings+1), 3])
        for i in range(rings):
            for j in range(nsides):
                next_i = i+1
                next_j = j+1
                # grid num
                grid_n = i * (nsides+1) + j
                # draw two triangles for each grid
                self.indices[2 * grid_n + 0] = [i * (nsides+1) + j,next_i * (nsides+1) + j, next_i * (nsides+1) + next_j]
                self.indices[2 * grid_n + 1] = [i * (nsides+1) + j,next_i * (nsides+1) + next_j, i * (nsides+1) + next_j]

    def draw(self):
        self.vao.bind()
        #self.vbo.draw()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems which don't enable a default VAO after GLProgram compilation
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
        self.vao.unbind()
