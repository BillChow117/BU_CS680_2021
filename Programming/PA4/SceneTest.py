"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA4
due date:                   Dec.07,2021

Scene for test
"""

"""
Define a fixed scene with rotating lights
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import math

import numpy as np

import ColorType
from Animation import Animation
from Component import Component
from DisplayableCylinder import DisplayableCylinder
from DisplayableEllipsoid import DisplayableEllipsoid
from Light import Light
from Material import Material
from Point import Point
import GLUtility

from DisplayableCube import DisplayableCube
from DisplayableTorus import DisplayableTorus
from DisplayableSphere import DisplayableSphere

##### TODO 1: Generate Triangle Meshes
# Requirements:
#   1. Use Element Buffer Object (EBO) to draw the cube. The cube provided in the start code is drawn with Vertex Buffer
#   Object (VBO). In the DisplayableCube class draw method, you should switch from VBO draw to EBO draw. To achieve
#   this, please first read through VBO and EBO classes in GLBuffer. Then you rewrite the self.vertices and self.indices
#   in the DisplayableCube class. Once you have all these down, then switch the line vbo.draw() to ebo.draw().
#   2. Generate Displayable classes for an ellipsoid, torus, and cylinder with end caps.
#   These classes should be like the DisplayableCube class and they should all use EBO in the draw method.
#   PS: You must use the ellipsoid formula to generate it, scaling the Displayable sphere doesn't count
#
#   Displayable object's self.vertices numpy matrix should be defined as this table:
#   Column | 0:3                | 3:6           | 6:9          | 9:11
#   Stores | Vertex coordinates | Vertex normal | Vertex Color | Vertex texture Coordinates
#
#   Their __init__ method should accept following input
#   arguments:
#   DisplayableEllipsoid(radiusInX, radiusInY, radiusInZ, slices, stacks)
#   DisplayableTorus(innerRadius, outerRadius, nsides, rings)
#   DisplayableCylinder(endRadius, height, slices, stacks)
#

##### TODO 5: Create your scenes
# Requirements:
#   1. We provide a fixed scene (SceneOne) for you with preset lights, material, and model parameters.
#   This scene will be used to examine your illumination implementation, and you should not modify it.
#   2. Create 3 new scenes (can be static scenes). Each of your scenes must have
#      * at least 3 differently shaped solid objects
#      * each object should have a different material
#      * at least 2 lights
#      * All types of lights should be used
#   3. Provide a keyboard interface that allows the user to toggle on/off each of the lights in your scene model:
#   Hit 1, 2, 3, 4, etc. to identify which light to toggle.


class SceneTest(Component):
    shaderProg = None
    glutility = None

    lights = None
    lightCubes = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        
        m1 = Material(np.array((0.0, 0.0, 0.0, 1.0)), np.array((1.0, 1.0, 1.0, 1.0)),
              np.array((1.0, 1.0, 1.0, 1.0)), 32)
        cube = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 1.5, 1, 1.5))
        cube.setMaterial(m1)
        cube.renderingRouting = "texture lighting normap"
        #cube.setTexture(shaderProg,'./assets/stoneWall.jpg')
        cube.setNormalMap(shaderProg,'./assets/normalmap.jpg')
        self.addChild(cube)

        # sphere = Component(Point((0,0,0)), DisplayableSphere(shaderProg, 1,18,36))
        # sphere.setMaterial(m1)
        # sphere.renderingRouting = "texture lighting normap"
        # sphere.setTexture(shaderProg,'./assets/earth.jpg')
        # sphere.setNormalMap(shaderProg,'./assets/normalmap.jpg')
        # self.addChild(sphere)
        
        # ellipsoid = Component(Point((0,0,0)), DisplayableEllipsoid(shaderProg, 1,1.2,1.4,18,36))
        # ellipsoid.setMaterial(m1)
        # ellipsoid.renderingRouting = "texture"
        # ellipsoid.setTexture(shaderProg,'./assets/cloudySphere.jpg')
        # self.addChild(ellipsoid)
        
        # cylinder = Component(Point((0,0,0)), DisplayableCylinder(shaderProg,0.3,2,18,36))
        # cylinder.setMaterial(m1)
        # cylinder.renderingRouting = "lighting"
        # self.addChild(cylinder)
        
        # torus = Component(Point((0,0,0)), DisplayableTorus(shaderProg,0.3,1.5,36,36,ColorType.WHITE))
        # torus.setMaterial(m1)
        # torus.renderingRouting = "texture lighting normap"
        # torus.setTexture(shaderProg,'./assets/marble.jpg')
        # torus.setNormalMap(shaderProg,'./assets/normalmap.jpg')
        # torus.rotate(90,torus.uAxis)
        # self.addChild(torus)

        # l0 = Light(Point([0.0, 1.5, 0.0]),
        #            np.array((*ColorType.WHITE, 1.0)),
        #            spotDirection=np.array([0.0,-1.0,0.0]))
        
        # l0 = Light(Point([0.0, 1.5, 0.0]),
        #            np.array((*ColorType.WHITE, 1.0)))
        
        l0 = Light(Point([0.0, 2, 0.0]),
           np.array((*ColorType.WHITE, 1.0)),
           infiniteDirection=Point((0,1,0)))
        
        lightCube0 = Component(Point((0.0, 2, 0.0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.WHITE))
        lightCube0.renderingRouting = "vertex"

        self.addChild(lightCube0)
        self.lights = [l0, ]
        self.lightCubes = [lightCube0, ]



    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
        
    def toggleLightType(self,light_type = ''):
        for i, light in enumerate(self.lights):
            if 'ambient' in light_type:
                light.ambientON = not light.ambientON
            if 'diffuse' in light_type:
                light.diffuseON = not light.diffuseON
            if 'specular' in light_type:
                light.specularON = not light.specularON

            self.shaderProg.setLight(i, light)
            
    def toggleLight(self, light:int = None ):
        if light >= len(self.lights): return
        self.lights[light].ambientON = not self.lights[light].ambientON
        self.lights[light].diffuseON = not self.lights[light].diffuseON
        self.lights[light].specularON = not self.lights[light].specularON
        
        for i, light in enumerate(self.lights):
            self.shaderProg.setLight(i, light)
