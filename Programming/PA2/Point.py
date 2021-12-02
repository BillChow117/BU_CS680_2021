"""
A Point class is defined here, which stores point coordinates, color and corresponding texture coordinates.
First version Created on 09/23/2018

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import copy
import time

from ColorType import ColorType


class Point:
    """
    Properties:
        coords: List<Integer>
        color: ColorType
        texture: List<Float>
    Desciption:
        Invisible Variables:
        coords is used to describe coordinates of a point, only integers allowed
        color is used to describe color of a point, must be ColorType Object
        texture is used to describe corresponding coordinates in texture, can be float or double
    """

    # Enforce type checking for all variables, set them invisible 
    coords = None
    color = None
    texture = None

    def __init__(self, coords=None, color=None, textureCoords=None):
        """
        init Point by using coords, __color, textureCoords or an existing point
        any missing argument will be set to all zero
        
        coords: list<int> or tuple<int>. 
        color: list or int or ColorType. 
        textureCoords: list or tuple.
        """
        # Be careful, Default dimension & dimensionT is 2
        self.setCoords(coords)
        self.setColor(color)
        self.setTextureCoords(textureCoords)


    def __repr__(self):
        return "p:" + str(self.getCoords()) + \
               " c:" + str(self.getColor()) + \
               " t:" + str(self.getTextureCoords())

    def __hash__(self):
        return hash((self.coords, self.color, self.texture))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        else:
            return self.coords == other.getCoords() and \
                    self.texture == other.getTextureCoords() and \
                    self.color == other.getColor()

    ################# Start of basic functions

    def setCoord(self, index, coordValue):
        """Set certain value in coords"""
        self.coords[index] = coordValue

    def setTextureCoord(self, index, coordValue):
        """Set a value in textureCoords"""
        self.texture[index] = coordValue

    def setColor(self, color):
        """
        Set point color

        :param color: Point's color
        :type color: ColorType
        :return: None
        """
        self.color = copy.deepcopy(color)

    def setColor_r(self, r):
        self.color.r = r

    def setColor_g(self, g):
        self.color.g = g

    def setColor_b(self, b):
        self.color.b = b

    def getDim(self):
        """
        get point coordinates dimension
        :return: point coordinates dimension, which is a non-negative integer
        """
        if self.coords is not None:
            return len(self.coords)
        else:
            return 0

    def getDimT(self):
        """
        get point texture coordinates dimension
        :return: point texture coordinates dimension, which is a non-negative integer
        """
        if self.texture is not None:
            return len(self.texture)
        else:
            return 0

    def getCoords(self):
        return self.coords

    def getTextureCoords(self):
        return self.texture

    def getColor(self):
        return self.color

    def setCoords(self, coords):
        """Use a tuple/list to set all values in coords"""
        self.coords = copy.deepcopy(coords)

    def setTextureCoords(self, textureCoords):
        """Use a tuple/list of coords to set all values in textureCoords"""
        self.texture = copy.deepcopy(textureCoords)

    def copy(self):
        newPoint = Point(copy.deepcopy(self.coords), copy.deepcopy(self.color), copy.deepcopy(self.texture))
        return newPoint

    ################# End of basic functions


if __name__ == "__main__":
    a = Point((1, 2))
    print(a)
    a.setColor((0.5, 0.2, 0.3))
    print(a)
    a.setCoords([3, 4])
    print(a)
    a.setTextureCoords((2.22, 3.33))
    print("Point a: ", a)
    b = a.copy()
    print("Point copied from point a: ", b)
    try:
        print("Test for illegal input")
        c = Point((1.5, 4))
    except:
        print("Get Error")

    # Test for list<Point>
    pl = [Point((1, 3)), Point((2, 3)),
          Point((3, 5))]
    print(pl)

    # Test for set<Point>
    ps = set(pl)
    print(ps)
    ps.add(Point((1, 3), ColorType(1, 0, 1)))
    print(ps)
    ps.add(Point((1, 3), ColorType(0, 0, 0)))
    print(ps)

    t1 = time.time()
    [Point() for _ in range(500 * 500)]
    print(time.time() - t1)
    t1 = time.time()
    for _ in range(500 * 500):
        a = Point()
    print(time.time() - t1)
    t1 = time.time()
    for _ in range(500 * 500):
        a = ColorType()
    print(time.time() - t1)
