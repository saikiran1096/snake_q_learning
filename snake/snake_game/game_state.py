import random
from collections import deque

import numpy as np

from snake.snake_game.location import Location


EMPTY_SYMBOL = 0
FOOD_SYMBOL = 1
HEAD_SYMBOL = 2
BODY_SYMBOL = 3
TAIL_SYMBOL = 4


class GameState:
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

    def __init__(self, shape):
        dim_x, dim_y = shape
        self.shape = shape
        self.board = np.zeros(shape, dtype=np.float32)

        start_loc = Location(random.randrange(dim_x), random.randrange(dim_y))
        self.snake = Snake(start_loc)
        self.board[start_loc.x, start_loc.y] = HEAD_SYMBOL

        self.game_over = False
        self.food_loc = self.new_food()
        self.score = 0

    def new_food(self):
        valid_locs = self.find_valid_locs()
        loc = random.choice(valid_locs)
        return loc

    def find_valid_locs(self):
        # generate all locs
        valid_locs = []
        for x in range(1, self.shape[0]):
            for y in range(1, self.shape[1]):
                # append if valid
                if Location(x, y) not in self.snake.locs:
                    valid_locs.append(Location(x, y))

        return valid_locs

    def make_move(self, move):
        new_loc = self.snake.head() + Location(*move)

        if not self.in_bounds(new_loc):
            self.score -= 1000
            self.game_over = True
            return -1000

        if self.snake.collides(new_loc):
            self.score -= 1000
            self.game_over = True
            return -1000

        if new_loc == self.food_loc:
            self.score += 100
            self.snake.eat(new_loc)
            self.food_loc = self.new_food()
            return 100

        else:
            self.score += 1
            self.snake.advance(new_loc)
            return 1

    def in_bounds(self, loc):
        return (0 <= loc.x < self.shape[0]) and (0 <= loc.y < self.shape[1])


class Snake:
    def __init__(self, start_loc):
        self.locs = deque([start_loc])

    def head(self):
        return self.locs[0]

    def tail(self):
        return self.locs[-1]

    def collides(self, loc):
        return loc in self.locs

    def length(self):
        return len(self.locs)

    def eat(self, loc):
        self.locs.appendleft(loc)

    def advance(self, loc):
        self.locs.appendleft(loc)
        self.locs.pop()
