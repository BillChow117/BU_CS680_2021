"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA4
due date:                   Dec.07,2021

Scene 3 of 3:
Objects: one sphere, one torus, one cube
Lights: one infinite light, one point light, one spot light
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
from DisplayableSphere import DisplayableSphere
from Light import Light
from Material import Material
from Point import Point
import GLUtility

from DisplayableCube import DisplayableCube
from DisplayableTorus import DisplayableTorus

class Scene3(Component, Animation):
    lights = None
    lightCubes = None
    shaderProg = None
    glutility = None

    lRadius = None
    lAngles = None
    lTransformations = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()
        
    
        m1 = Material(np.array([0.1,0.1,0.1,1.0]),
                      np.array([1.0,1.0,1.0,1.0]),
                      np.array([0.3,0.3,0.3,1.0]), 64)
        sphere = Component(Point((0.7,0,0)), DisplayableSphere(shaderProg, 0.5,36,36))
        sphere.setMaterial(m1)
        sphere.renderingRouting = "lighting texture normap"
        sphere.setTexture(shaderProg,'./assets/earth.jpg')
        sphere.setNormalMap(shaderProg,'./assets/normalmap.jpg')
        self.sphere_vangle = 0
        self.sphere = sphere
        self.addChild(sphere)

        m2 = Material(np.array([0.1,0.1,0.1, 1.0]),
                      np.array([0.3,0.3,0.3, 1.0]),
                      np.array([1.0,1.0,1.0, 1.0]), 64)
        torus = Component(Point((0, 0, -1.0)), DisplayableTorus(shaderProg, 0.25, 1.0, 36, 36))
        torus.setMaterial(m2)
        torus.renderingRouting = "lighting texture normap"
        torus.setTexture(shaderProg,'./assets/marble.jpg')
        torus.setNormalMap(shaderProg,'./assets/normalmap.jpg')
        self.torus = torus
        self.addChild(torus)
        
        m3 = Material(np.array([0.0, 0.0, 0.0, 1.0]),
                      np.array([1.0, 1.0, 1.0, 1.0]),
                      np.array([0.0, 0.0, 0.0, 1.0]), 32)
        cube = Component(Point((-1, 0, 0)), DisplayableCube(shaderProg, 1.0, 1.0, 1.0))
        cube.setMaterial(m3)
        cube.renderingRouting = "texture lighting normap"
        cube.setTexture(shaderProg,'./assets/stoneWall.jpg')
        cube.setNormalMap(shaderProg,'./assets/normalmap.jpg')
        self.addChild(cube)
        
        l0 = Light(Point((0,0,0)),
                    np.array((*ColorType.WHITE, 1.0)))
        lightCube0 = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 0.1,0.1,0.1, ColorType.WHITE))
        lightCube0.renderingRouting = "vertex"
        self.addChild(lightCube0)
        
        l1 = Light(Point((1,1,0)),
                    np.array((*ColorType.WHITE, 1.0)),
                    spotDirection=np.array([-1.0,-1.0,0.0]),
                    spotRadialFactor=np.array([0.1,0.1,0.1]),
                    spotAngularFactor=8,
                    spotAngleLimit=30)
        lightCube1 = Component(Point((1, 1, 0)), DisplayableCube(shaderProg, 0.1,0.1,0.1, ColorType.WHITE))
        lightCube1.renderingRouting = "vertex"
        self.addChild(lightCube1)

        inffniteLight = Light(Point([0,0,0]),color=np.array((*ColorType.WHITE, 1.0)), infiniteDirection=Point([-1,1,1]))
        
        self.lights = [l0,l1,inffniteLight]
        self.lightCubes = [lightCube0,lightCube1]

    def lightPos(self, radius, thetaAng, transformationMatrix):
        r = np.zeros(4)
        r[0] = radius * math.cos(thetaAng / 180 * math.pi)
        r[2] = radius * math.sin(thetaAng / 180 * math.pi)
        r[3] = 1
        r = transformationMatrix @ r
        return r[0:3]

    def animationUpdate(self):        
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)


        for c in self.children:
            if isinstance(c, Animation):
                c.animationUpdate()

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
        
    # toggle ambient, diffuse, specular
    def toggleLightType(self,light_type:str = ''):
        for i, light in enumerate(self.lights):
            if 'ambient' in light_type:
                light.ambientON = not light.ambientON
            if 'diffuse' in light_type:
                light.diffuseON = not light.diffuseON
            if 'specular' in light_type:
                light.specularON = not light.specularON
                
            self.shaderProg.setLight(i, light)
            
    # toggle one light
    def toggleLight(self, light:int = None ):
        if light >= len(self.lights): return
        self.lights[light].ambientON = not self.lights[light].ambientON
        self.lights[light].diffuseON = not self.lights[light].diffuseON
        self.lights[light].specularON = not self.lights[light].specularON

        for i, light in enumerate(self.lights):
            self.shaderProg.setLight(i, light)