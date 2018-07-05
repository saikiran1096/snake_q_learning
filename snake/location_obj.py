"""
snake/location_obj.py

author:         Stephen Radley
date:           2018/07/05
package:        snake
version:        0.0.1
"""


"""
Location ...
"""
class Location:

    """
    __init__ ...
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    """
    collided ...
    """
    def collided(self, loc):
        if loc.x == self.x and loc.y == self.y:
            return True
        return False