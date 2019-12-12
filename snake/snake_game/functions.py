"""
snake/functions.py

author:         Stephen Radley
date:           2018/07/05
package:        snake
version:        0.0.1
"""

import curses


"""
is_allowed_key ...
"""
def is_allowed_key(key):
    allowed_keys = [
        curses.KEY_LEFT,
        curses.KEY_RIGHT,
        curses.KEY_UP,
        curses.KEY_DOWN
    ]

    if key in allowed_keys:
        return True

    return False


"""
is_opposite_key ...
"""
def is_opposite_key(curr_key, key):
    if curr_key == curses.KEY_LEFT:
        if key == curses.KEY_RIGHT:
            return True

    if curr_key == curses.KEY_RIGHT:
        if key == curses.KEY_LEFT:
            return True

    if curr_key == curses.KEY_UP:
        if key == curses.KEY_DOWN:
            return True

    if curr_key == curses.KEY_DOWN:
        if key == curses.KEY_UP:
            return True

    return False


"""
find_valid_locs ...
"""
def find_valid_locs(dim_x, dim_y, snake):
    # generate snake locs
    snake_locs = []
    for loc in snake.locs:
        snake_locs.append((loc.x, loc.y))

    # generate all locs
    valid_locs = []
    for x in range(1, dim_x - 1):
        for y in range(1, dim_y - 1):
            # append if valid
            if (x, y) not in snake_locs:
                valid_locs.append((x, y))

    return valid_locs