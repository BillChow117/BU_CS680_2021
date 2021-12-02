'''
Define an abstract class Displayable here.
First version in 09/26/2018

:author: micou(Zezhou Sun)
:version: 2021.1.1
'''


class Displayable:
    """
    Interface for displayable object
    """
    callListHandle = 0  # the display list handle, which is a integer
    parent = None  # the parent object, which has the opengl context

    def __init__(self, parent):
        self.parent = parent

    def draw(self):
        raise NotImplementedError

    def initialize(self):
        raise NotImplementedError
