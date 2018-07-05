"""
snake/snake_obj.py

author:         Stephen Radley
date:           2018/07/05
package:        snake
version:        0.0.1
"""

import curses
from snake.location_obj import Location


"""
Snake ...
"""
class Snake:

    """
    __init__ ...
    """
    def __init__(self, dim_x, dim_y, start_len=1):
        # set max dimensions
        self.max_x, self.max_y = dim_x - 1, dim_y - 1

        # set location
        first_loc = Location(int(self.max_x / 2), int(self.max_y / 2))
        self.locs = [first_loc]

        # set length
        self.length = start_len

    """
    move ...
    """
    def move(self, move_x, move_y):
        # check out of bounds x
        if (self.locs[0].x + move_x < 1 or
                self.locs[0].x + move_x >= self.max_x):
            return False

        # check out of bounds y
        if (self.locs[0].y + move_y < 1 or
                self.locs[0].y + move_y >= self.max_y):
            return False

        # set new location
        new_loc = Location(self.locs[0].x + move_x, self.locs[0].y + move_y)

        # check for collision with self
        for loc in self.locs:
            if loc.collided(new_loc):
                return False

        # insert new location
        self.locs.insert(0, new_loc)

        # delete old location
        self.locs = self.locs[:self.length]

        return True

    """
    move_direction ...
    """
    def move_in_direction(self, key):
        if key == curses.KEY_RIGHT:
            return self.move(1, 0)

        if key == curses.KEY_LEFT:
            return self.move(-1, 0)

        if key == curses.KEY_UP:
            return self.move(0, -1)

        if key == curses.KEY_DOWN:
            return self.move(0, 1)

        return False

    """
    eat ...
    """
    def eat(self):
        self.length += 1

    """
    copy ...
    """
    def copy(self):
        copy_snake = Snake(self.max_x, self.max_y)
        copy_snake.locs = self.locs
        copy_snake.length = self.length
        return copy_snake