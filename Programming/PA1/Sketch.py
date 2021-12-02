"""
Name:                       Yumiao Zhou
the class:                  CS680
the assignment number:      PA1
due date:                   Sep.21,2021

"""

"""
This is the main entry of your program. Almost all things you need to implement are in this file.
The main class Sketch inherits from CanvasBase. For the parts you need to implement, they are all marked with TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun)
:version: 2021.2.1

"""

import os

import wx
import math
import random
import numpy as np
from wx.core import Sleep

from Buff import Buff
from Point import Point
from ColorType import ColorType
from CanvasBase import CanvasBase

try:
    # From pip package "Pillow"
    from PIL import Image
except Exception:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError


class Sketch(CanvasBase):
    """
    Drawing methods and interrupt methods will be implemented in this class.
    
    Class Variable Explanation:

    * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will print more details and do some type checking, which might be helpful in debugging
    
    * texture(Buff): loaded texture in Buff instance
    * random_color(bool): Control flag of random color generation of point.
    * doTexture(bool): Control flag of doing texture mapping
    * doSmooth(bool): Control flag of doing smooth
    * doAA(bool): Control flag of doing anti-aliasing
    * doAAlevel(int): anti-alising supersampling level
        
    Method Instruction:

    * Interrupt_MouseL(R): Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
    * Interrupt_Keyboard: Used to deal with keyboard press interruption. Use this to add new keys or new methods
    * drawPoint: method to draw a point
    * drawLine: method to draw a line
    * drawTriangle: method to draw a triangle with filling and smoothing
    
    List of interrupt methods, which defined keyboard and mouse operations:

    * Interrupt_MouseL
    * Interrupt_MouseR
    * Interrupt_Keyboard
        
    Here are some public variables in parent class you might need:

    * points_r: list<Point>. to store all Points from Mouse Right Button
    * points_l: list<Point>. to store all Points from Mouse Left Button
    * buff    : Buff. buff of current frame. Change on it will change display on screen
    * buff_last: Buff. Last frame buffer
        
    """

    debug = 0
    texture_file_path = "./pattern.jpg"
    texture = None

    # control flags
    randomColor = False
    doTexture = False
    doSmooth = False
    doAA = False
    doAAlevel = 4

    # test case status
    MIN_N_STEPS = 6
    MAX_N_STEPS = 192
    n_steps = 12  # For test case only
    test_case_index = 0
    test_case_list = []  # If you need more test case, write them as a method and add it to list

    def __init__(self, parent):
        """
        Initialize the instance, load texture file to Buff, and load test cases.
        You shouldn't create your own instance, this has already been prepared for you in the __main__.

        :param parent: wxpython frame
        :type parent: wx.Frame
        """
        super(Sketch, self).__init__(parent)
        self.test_case_list = [lambda _: self.clear(),
                               self.testCaseLine01,
                               self.testCaseLine02,
                               self.testCaseTri01,
                               self.testCaseTri02,
                               self.testCaseTriTexture01]  # method at here must accept one argument, n_steps
        # Try to read texture file
        if os.path.isfile(self.texture_file_path):
            # Read image and make it to an ndarray
            texture_image = Image.open(self.texture_file_path)
            texture_array = np.array(texture_image).astype(np.uint8)
            # Because imported image is upside down, reverse it
            texture_array = np.flip(texture_array, axis=0)
            # Store texture image in our Buff format
            self.texture = Buff(texture_array.shape[1], texture_array.shape[0])
            self.texture.setStaticBuffArray(np.transpose(texture_array, (1, 0, 2)))
            if self.debug > 0:
                print("Texture Loaded with shape: ", texture_array.shape)
                print("Texture Buff have size: ", self.texture.size)
        else:
            raise ImportError("Cannot import texture file")

    def __addPoint2Pointlist(self, pointlist, x, y):
        if self.randomColor:
            p = Point((x, y), ColorType(random.random(), random.random(), random.random()))
        else:
            p = Point((x, y), ColorType(1, 0, 0))
        pointlist.append(p)

    # Deal with Mouse Left Button Pressed Interruption
    def Interrupt_MouseL(self, x, y):
        self.__addPoint2Pointlist(self.points_l, x, y)
        # Draw a point when one point provided or a line when two ends provided
        if len(self.points_l) % 2 == 1:
            if self.debug > 0:
                print("draw a point", self.points_l[-1])
            self.drawPoint(self.buff, self.points_l[-1])
        elif len(self.points_l) % 2 == 0 and len(self.points_l) > 0:
            if self.debug > 0:
                print("draw a line from ", self.points_l[-2], " -> ", self.points_l[-1])
            #self.drawPoint(self.buff, self.points_l[-1])
            self.drawLine(self.buff,self.points_l[-2],self.points_l[-1])
            self.points_l.clear()

    # Deal with Mouse Right Button Pressed Interruption
    def Interrupt_MouseR(self, x, y):
        self.__addPoint2Pointlist(self.points_r, x, y)
        if len(self.points_r) % 3 == 1:
            if self.debug > 0:
                print("draw a point", self.points_r[-1])
            self.drawPoint(self.buff, self.points_r[-1])
        elif len(self.points_r) % 3 == 2:
            if self.debug > 0:
                print("draw a line from ", self.points_r[-2], " -> ", self.points_r[-1])
            #self.drawPoint(self.buff, self.points_r[-1])
            self.drawLine(self.buff,self.points_r[-2],self.points_r[-1])
        elif len(self.points_r) % 3 == 0 and len(self.points_r) > 0:
            if self.debug > 0:
                print("draw a triangle {} -> {} -> {}".format(self.points_r[-3], self.points_r[-2], self.points_r[-1]))
            #self.drawPoint(self.buff, self.points_r[-1])
            self.drawTriangle(self.buff,self.points_r[-3],self.points_r[-2],self.points_r[-1])
            self.points_r.clear()

    def Interrupt_Keyboard(self, keycode):
        """
        keycode Reference: https://docs.wxpython.org/wx.KeyCode.enumeration.html#wx-keycode

        * r, R: Generate Random Color point
        * c, C: clear buff and screen
        * LEFT, UP: Last Test case
        * t, T, RIGHT, DOWN: Next Test case
        """
        # Trigger for test cases
        if keycode in [wx.WXK_LEFT, wx.WXK_UP]:  # Last Test Case
            self.clear()
            if len(self.test_case_list) != 0:
                self.test_case_index = (self.test_case_index - 1) % len(self.test_case_list)
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if keycode in [ord("t"), ord("T"), wx.WXK_RIGHT, wx.WXK_DOWN]:  # Next Test Case
            self.clear()
            if len(self.test_case_list) != 0:
                self.test_case_index = (self.test_case_index + 1) % len(self.test_case_list)
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if chr(keycode) in ",<":
            self.clear()
            self.n_steps = max(self.MIN_N_STEPS, round(self.n_steps / 2))
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if chr(keycode) in ".>":
            self.clear()
            self.n_steps = min(self.MAX_N_STEPS, round(self.n_steps * 2))
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if keycode in [wx.WXK_SPACE]:
            self.clear()
            self.__addPoint2Pointlist(self.points_l,100,100)
            self.__addPoint2Pointlist(self.points_l,200,201)
            self.drawLine(self.buff,self.points_l[-2],self.points_l[-1])
            self.points_l.clear()
            self.__addPoint2Pointlist(self.points_l,100,101)
            self.__addPoint2Pointlist(self.points_l,200,202)
            self.drawLine(self.buff,self.points_l[-1],self.points_l[-2])

        # Switches
        if chr(keycode) in "rR":
            self.randomColor = not self.randomColor
            print("Random Color: ", self.randomColor)
        if chr(keycode) in "cC":
            self.clear()
            print("clear Buff")
        if chr(keycode) in "sS":
            self.doSmooth = not self.doSmooth
            print("Do Smooth: ", self.doSmooth)
        if chr(keycode) in "aA":
            self.doAA = not self.doAA
            print("Do Anti-Aliasing: ", self.doAA)
        if chr(keycode) in "mM":
            self.doTexture = not self.doTexture
            print("texture mapping: ", self.doTexture)

    def queryTextureBuffPoint(self, texture: Buff, x: int, y: int) -> Point:
        """
        Query a point at texture buff, should only be used in texture buff query

        :param texture: The texture buff you want to query from
        :type texture: Buff
        :param x: The query point x coordinate
        :type x: int
        :param y: The query point y coordinate
        :type y: int
        :rtype: Point
        """
        if self.debug > 1:
            if x != min(max(0, int(x)), texture.width - 1):
                print("Warning: Texture Query x coordinate outbound")
            if y != min(max(0, int(y)), texture.height - 1):
                print("Warning: Texture Query y coordinate outbound")
        return texture.getPointFromPointArray(x, y)

    @staticmethod
    def drawPoint(buff, point):
        """
        Draw a point on buff

        :param buff: The buff to draw point on
        :type buff: Buff
        :param point: A point to draw on buff
        :type point: Point
        :rtype: None
        """
        x, y = point.coords
        c = point.color
        # because we have already specified buff.buff has data type uint8, type conversion will be done in numpy
        buff.buff[x, y, 0] = c.r * 255
        buff.buff[x, y, 1] = c.g * 255
        buff.buff[x, y, 2] = c.b * 255

    def drawLine(self, buff, p1, p2, doSmooth=True, doAA=False, doAAlevel=4):
        """
        Draw a line between p1 and p2 on buff

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: One end point of the line
        :type p1: Point
        :param p2: Another end point of the line
        :type p2: Point
        :param doSmooth: Control flag of color smooth interpolation
        :type doSmooth: bool
        :param doAA: Control flag of doing anti-aliasing
        :type doAA: bool
        :param doAAlevel: anti-aliasing super sampling level
        :type doAAlevel: int
        :rtype: None
        """
        ##### TODO 1: Use Bresenham algorithm to draw a line between p1 and p2 on buff.
        # Requirements:
        #   1. Only integer is allowed in interpolate point coordinates between p1 and p2
        #   2. Float number is allowed in interpolate point color

        # using the generator get coordinates and colors of points to draw
        for point in self.drawLine_Generator(buff, p1, p2, doSmooth=True, doAA=False, doAAlevel=4):
            self.drawPoint(buff,point)

        return

    # to use the draw line method in the draw triangle funciton, I split it into two parts
    def drawLine_Generator(self, buff, p1, p2, doSmooth=True, doAA=False, doAAlevel=4):
        """
        Each iteration yield a point on the line from p1 to p2

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: Start point of the line
        :type p1: Point
        :param p2: End point of the line
        :type p2: Point
        :param doSmooth: Control flag of color smooth interpolation
        :type doSmooth: bool
        :param doAA: Control flag of doing anti-aliasing
        :type doAA: bool
        :param doAAlevel: anti-aliasing super sampling level
        :type doAAlevel: int
        :rtype: Point
        """
        p1x, p1y = p1.coords
        p2x, p2y = p2.coords
        
        dx = p2x - p1x
        dy = p2y - p1y
        abs2dx = 2 * abs(dx)
        abs2dy = 2 * abs(dy)

        if abs2dx >= abs2dy:                                            # render with growth of x
            P = abs2dy - abs(dx)                                        # determing factor
            yi = p1y
            x_step = 1 if dx > 0 else -1
            y_step = 1 if dy > 0  else -1
            for xi in range(p1x,p2x+y_step,x_step):
                
                p1_colorProp= (p2x-xi)/(p2x-p1x)                        # color propotion of p1
                p2_colorProp = 1 - p1_colorProp                         # color propotion of p2

                yield Point((xi,yi),ColorType(p1.color.r * p1_colorProp + p2.color.r * p2_colorProp,p1.color.g * p1_colorProp + p2.color.g * p2_colorProp,p1.color.b * p1_colorProp + p2.color.b * p2_colorProp))

                if P >= 0:
                    yi += y_step
                    P -= abs2dx                                         # calibate the factor
                P += abs2dy

        else:                                                           # render with growth of y
            P = abs2dx - abs(dy)                       
            xi = p1x
            y_step = 1 if dy > 0 else -1
            x_step = 1 if dx > 0  else -1
            for yi in range(p1y,p2y+y_step,y_step):
                
                p1_colorProp= (p2y-yi)/(p2y-p1y)                       
                p2_colorProp = 1 - p1_colorProp  

                yield Point((xi,yi),ColorType(p1.color.r * p1_colorProp + p2.color.r * p2_colorProp,p1.color.g * p1_colorProp + p2.color.g * p2_colorProp,p1.color.b * p1_colorProp + p2.color.b * p2_colorProp))
                
                if P >= 0:
                    xi += x_step
                    P -= abs2dy                                 
                P += abs2dx  

        return

    def drawTriangle(self, buff, p1, p2, p3, doSmooth=True, doAA=False, doAAlevel=4, doTexture=False):
        """
        draw Triangle to buff. apply smooth color filling if doSmooth set to true, otherwise fill with first point color
        if doAA is true, apply anti-aliasing to triangle based on doAAlevel given.

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: First triangle vertex
        :param p2: Second triangle vertex
        :param p3: Third triangle vertex
        :type p1: Point
        :type p2: Point
        :type p3: Point
        :param doSmooth: Color smooth filling control flag
        :type doSmooth: bool
        :param doAA: Anti-aliasing control flag
        :type doAA: bool
        :param doAAlevel: Anti-aliasing super sampling level
        :type doAAlevel: int
        :param doTexture: Draw triangle with texture control flag
        :type doTexture: bool
        :rtype: None
        """
        ##### TODO 2: Write a triangle rendering function, which support smooth bilinear interpolation of the vertex color
        ##### TODO 3(For CS680 Students): Implement texture-mapped fill of triangle. Texture is stored in self.texture
        # Requirements:
        #   1. For flat shading of the triangle, use the first vertex color.
        #   2. Polygon scan fill algorithm and the use of barycentric coordinate are not allowed in this function
        #   3. You should be able to support both flat shading and smooth shading, which is controlled by doSmooth
        #   4. For texture-mapped fill of triangles, it should be controlled by doTexture flag.
        if not doSmooth:
            p2.color = p1.color
            p3.color = p1.color

        point_list = [p1,p2,p3]
        TOP_list = [] 
        BOTTOM_list = []
        p1x,p1y = p1.coords
        p2x,p2y = p2.coords
        p3x,p3y = p3.coords

        # the transform matrix used in the future
        TransMtx = np.empty((3,3))

        if doTexture:
            # assuming R is the minimum bounding rectangle of the triangle. R1,R2 are left-bottom and right-top points, respectively.
            R1x = min(p1x,p2x,p3x)
            R1y = min(p1y,p2y,p3y)
            R2x = max(p1x,p2x,p3x)
            R2y = max(p1y,p2y,p3y)

            R_width = R2x - R1x + 1
            R_height = R2y- R1y + 1

            # No.1 Method
            # Make a T2ST1 transform trun R to a maximun inscribed rectangle of Texture space wihle keep its ratio, to get the coords in Texture

            # R_width/R_height < T_width/T_height
            if R_width/R_height < self.texture.width/self.texture.height:
                # T( -R1x - R.w/2 , -R1y )
                T1 = np.array([[1,0,-R1x-R_width/2],
                                [0,1,-R1y],
                                [0,0,1]])
                # S( T.h/R.h , T.h/R.h )
                S = np.array([[self.texture.height/R_height,0,0],
                                [0,self.texture.height/R_height,0],
                                [0,0,1]])
                # T( T.w/2 , 0 )
                T2 = np.array([[1,0,self.texture.width/2],
                                [0,1,0],
                                [0,0,1]])
            # R_width/R_height >= T_width/T_height
            else:
                # T( -R1x , -R1y -R.h/2 )
                T1 = np.array([[1,0,-R1x],
                                [0,1,-R1y-R_height/2],
                                [0,0,1]])
                # S( T.w/R.w , T.w/R.w )
                S = np.array([[self.texture.width/R_width,0,0],
                                [0,self.texture.width/R_width,0],
                                [0,0,1]])
                # T( 0 , T.h/2 )
                T2 = np.array([[1,0,0],
                                [0,1,self.texture.height/2],
                                [0,0,1]])

            tmp = np.dot(S,T1)
            TransMtx = np.dot(T2,tmp)

            # # No.2 Method
            # # Make a ST transform trun R to as same size as Texture, to get the coords in Texture
            # # T( R1x , R1y )
            # T = np.array([[1,0,-R1x],
            #             [0,1,-R1y],
            #             [0,0,1]])

            # # S( Texture.width/R.width , Texture.height/R.height )
            # S = np.array([[self.texture.width/R_width,0,0],
            #                 [0,self.texture.height/R_height,0],
            #                 [0,0,1]])

            # TransMtx = np.dot(S,T)

        # find the top/bottom point
        for point in point_list:
            if point.coords[1] == max(p1y,p2y,p3y):
                TOP_list.append(point)
            if point.coords[1] == min(p1y,p2y,p3y):
                BOTTOM_list.append(point)

        if len(TOP_list) > 1:           # Top Flat Triangle
            self.drawFlatTriangle(buff,BOTTOM_list[0],TOP_list[0],TOP_list[1],doSmooth, doAA, doAAlevel, doTexture, TransMtx)
        elif len(BOTTOM_list) > 1:      # Bottom Flat Triangle
            self.drawFlatTriangle(buff,TOP_list[0],BOTTOM_list[0],BOTTOM_list[1],doSmooth, doAA, doAAlevel, doTexture, TransMtx)
        else:                           # Normal Triangle
            a = TOP_list[0]
            c = BOTTOM_list[0]
            point_list.remove(a)
            point_list.remove(c)
            b = point_list[0]           

            ax,ay = a.coords
            bx,by = b.coords
            cx,cy = c.coords

            dx = round(ax + ((ay - by) * (cx - ax)) / (ay - cy))    # (dx - ax) / (cx - ax) = (ay - by) / (ay - cy)
            dy = by

            a_colorProp = (cy-dy)/(cy-ay) 
            c_colorProp = 1 - a_colorProp

            # points b and d split the original triangle into a bottom flat triangle and a top flat triangle
            d = Point((dx,dy),ColorType(a.color.r * a_colorProp + c.color.r * c_colorProp,a.color.g * a_colorProp + c.color.g * c_colorProp,a.color.b * a_colorProp + c.color.b * c_colorProp))

            self.drawFlatTriangle(buff,a,b,d,doSmooth, doAA, doAAlevel, doTexture, TransMtx)
            self.drawFlatTriangle(buff,c,b,d,doSmooth, doAA, doAAlevel, doTexture, TransMtx)

        return

    # get the point mapping in Texture 
    def getPointinTexture(self,x,y,TransformMatrix):
        """
        return the point in texture based on the coordinates of the point in triangle

        :param x: x coordinate
        :type x: int
        :param y: y coordinate
        :type y: int
        :param TransformMatrix: Transform Matrix
        :type TransformMatrix: ndarray
        :rtype: Point
        """
        # v1 is the coords-vector of point
        v1 = np.array([x,y,1])
        # v2 is the coords-vector of point in Texture space
        v2 = np.dot(TransformMatrix,v1)
        Texel = self.queryTextureBuffPoint(self.texture,int(v2.item(0)),int(v2.item(1)))
        return Point((x,y),Texel.color)

    # draw a flat triangle
    def drawFlatTriangle(self,buff,p1,p2,p3,doSmooth=True, doAA=False, doAAlevel=4, doTexture=False, TransformMatrix = None):
        """
        draw Flat Triangle to buff. apply smooth color filling if doSmooth set to true, apply anti-aliasing to triangle based on doAAlevel given.

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: Top/Bottom vertex
        :param p2: An end point on the flat edge of the triangle
        :param p3: Another end point on the flat edge of the triangle
        :type p1: Point
        :type p2: Point
        :type p3: Point
        :param doSmooth: Color smooth filling control flag
        :type doSmooth: bool
        :param doAA: Anti-aliasing control flag
        :type doAA: bool
        :param doAAlevel: Anti-aliasing super sampling level
        :type doAAlevel: int
        :param doTexture: Draw triangle with texture control flag
        :type doTexture: bool
        :param TransformMatrix: Transform Matrix
        :type TransformMatrix: ndarray
        :rtype: None
        """
        top = p1.coords[1]
        bottom = p2.coords[1]
        height = top - bottom                   # Height of the triangle

        # flat lines growth dirction based on p1's position
        y_step = 1 if height < 0 else -1

        # two generators, return every point on two edges
        ab_gen = self.drawLine_Generator(buff,p1,p2,doSmooth, doAA, doAAlevel)
        ac_gen = self.drawLine_Generator(buff,p1,p3,doSmooth, doAA, doAAlevel)

        # the start points
        ab = next(ab_gen)
        ac = next(ac_gen)
        self.drawPoint(buff,ab)
        self.drawPoint(buff,ac)

        # fill by texture
        if doTexture and isinstance(TransformMatrix,np.ndarray):
            for curr_y in range(top+y_step,bottom+y_step,y_step):
                while ab.coords[1] != curr_y:
                    try:
                        # ab is the current point on line ab
                        ab = next(ab_gen)
                    except StopIteration:
                        break
                    
                    todraw = self.getPointinTexture(ab.coords[0],ab.coords[1],TransformMatrix)
                    self.drawPoint(buff,todraw)

                while ac.coords[1] != curr_y:
                    try:
                        ac = next(ac_gen)
                    except StopIteration:
                        break
                    
                    todraw = self.getPointinTexture(ac.coords[0],ac.coords[1],TransformMatrix)
                    self.drawPoint(buff,todraw)

                abx,aby = ab.coords
                acx,acy = ac.coords
                dx = acx - abx
                if dx != 0:
                    # draw a flat line
                    x_step = 1 if dx > 0 else -1
                    for curr_x in range(abx,acx+x_step,x_step):
                        todraw = self.getPointinTexture(curr_x,curr_y,TransformMatrix)
                        self.drawPoint(buff,todraw)

        # fill by smooth color
        else:
            for curr_y in range(top+y_step,bottom+y_step,y_step):
                while ab.coords[1] != curr_y:
                    try:
                        ab = next(ab_gen)
                    except StopIteration:
                        break
                    self.drawPoint(buff,ab)
                while ac.coords[1] != curr_y:
                    try:
                        ac = next(ac_gen)
                    except StopIteration:
                        break
                    self.drawPoint(buff,ac)

                abx,aby = ab.coords
                acx,acy = ac.coords
                dx = acx - abx
                if dx != 0:
                    # draw a flat line
                    x_step = 1 if dx > 0 else -1
                    for curr_x in range(abx,acx+x_step,x_step):
                        ab_colorProp = (acx-curr_x)/(acx-abx) 
                        ac_colorProp = 1 - ab_colorProp
                        x = Point((curr_x,curr_y),ColorType(ab.color.r * ab_colorProp + ac.color.r * ac_colorProp,ab.color.g * ab_colorProp + ac.color.g * ac_colorProp,ab.color.b * ab_colorProp + ac.color.b * ac_colorProp))
                        self.drawPoint(buff,x)

        return

    # test for lines lines in all directions
    def testCaseLine01(self, n_steps):
        center_x = int(self.buff.width / 2)
        center_y = int(self.buff.height / 2)
        radius = int(min(self.buff.width, self.buff.height) * 0.45)

        v0 = Point([center_x, center_y], ColorType(1, 1, 0))
        for step in range(0, n_steps):
            theta = math.pi * step / n_steps
            v1 = Point([center_x + int(math.sin(theta) * radius), center_y + int(math.cos(theta) * radius)],
                       ColorType(0, 0, (1 - step / n_steps)))
            v2 = Point([center_x - int(math.sin(theta) * radius), center_y - int(math.cos(theta) * radius)],
                       ColorType(0, (1 - step / n_steps), 0))
            self.drawLine(self.buff, v2, v0, doSmooth=True)
            self.drawLine(self.buff, v0, v1, doSmooth=True)

    # test for lines: drawing circle and petal 
    def testCaseLine02(self, n_steps):
        n_steps = 2 * n_steps
        d_theta = 2 * math.pi / n_steps
        d_petal = 12 * math.pi / n_steps
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        radius = (0.75 * min(cx, cy))
        p = radius * 0.25

        # Outer petals
        for i in range(n_steps + 2):
            self.drawLine(self.buff,
                          Point((math.floor(0.5 + radius * math.sin(d_theta * i) + p * math.sin(d_petal * i)) + cx,
                                 math.floor(0.5 + radius * math.cos(d_theta * i) + p * math.cos(d_petal * i)) + cy),
                                ColorType(1, (128 + math.sin(d_theta * i * 5) * 127 / 255),
                                          (128 + math.cos(d_theta * i * 5) * 127 / 255))),
                          Point((math.floor(
                              0.5 + radius * math.sin(d_theta * (i + 1)) + p * math.sin(d_petal * (i + 1))) + cx,
                                 math.floor(0.5 + radius * math.cos(d_theta * (i + 1)) + p * math.cos(
                                     d_petal * (i + 1))) + cy),
                                ColorType(1, (128 + math.sin(d_theta * 5 * (i + 1)) * 127 / 255),
                                          (128 + math.cos(d_theta * 5 * (i + 1)) * 127 / 255))),
                          doSmooth=True, doAA=self.doAA, doAAlevel=self.doAAlevel)

        # Draw circle
        for i in range(n_steps + 1):
            v0 = Point((math.floor(0.5 * radius * math.sin(d_theta * i)) + cx,
                        math.floor(0.5 * radius * math.cos(d_theta * i)) + cy), ColorType(1, 97. / 255, 0))
            v1 = Point((math.floor(0.5 * radius * math.sin(d_theta * (i + 1))) + cx,
                        math.floor(0.5 * radius * math.cos(d_theta * (i + 1))) + cy), ColorType(1, 97. / 255, 0))
            self.drawLine(self.buff, v0, v1, doSmooth=True, doAA=self.doAA, doAAlevel=self.doAAlevel)

    # test for smooth filling triangle
    def testCaseTri01(self, n_steps):
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            self.drawTriangle(self.buff, v1, v0, v2, False, self.doAA, self.doAAlevel)

    def testCaseTri02(self, n_steps):
        # Test case for no smooth color filling triangle
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            self.drawTriangle(self.buff, v0, v1, v2, True, self.doAA, self.doAAlevel)

    def testCaseTriTexture01(self, n_steps):
        # Test case for no smooth color filling triangle
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        triangleList = []
        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            triangleList.append([v0, v1, v2])

        for t in triangleList:
            self.drawTriangle(self.buff, *t, doTexture=True)


if __name__ == "__main__":
    def main():
        print("This is the main entry! ")
        app = wx.App(False)
        # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame
        # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
        # wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER will disable canvas resize.
        frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)

        canvas = Sketch(frame)
        canvas.debug = 0

        frame.Show()
        app.MainLoop()


    def codingDebug():
        """
        If you are still working on the assignment, we suggest to use this as the main call.
        There will be more strict type checking in this version, which might help in locating your bugs.
        """
        print("This is the debug entry! ")
        import cProfile
        import pstats
        profiler = cProfile.Profile()
        profiler.enable()

        app = wx.App(False)
        # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame
        # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
        # wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER will disable canvas resize.
        frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
        canvas = Sketch(frame)
        canvas.debug = 0
        frame.Show()
        app.MainLoop()

        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime').reverse_order()
        stats.print_stats()


    main()
    # codingDebug()
