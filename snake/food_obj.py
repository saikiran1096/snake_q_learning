"""
snake/food_obj.py

author:         Stephen Radley
date:           2018/07/05
package:        snake
version:        0.0.1
"""

from random import randint

from snake.location_obj import Location
from snake.functions import find_valid_locs


"""
Food ...
"""
class Food:

    """
    __init__ ...
    """
    def __init__(self, dim_x, dim_y, snake):
        valid_locs = find_valid_locs(dim_x, dim_y, snake)
        loc = valid_locs[randint(0, len(valid_locs)-1)]
        self.loc = Location(loc[0], loc[1])