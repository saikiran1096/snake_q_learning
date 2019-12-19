import curses
import sys
import time
import logging

from snake.snake_game.game_state import GameState


def key_to_move(key):
    if key == curses.KEY_RIGHT:
        return GameState.RIGHT

    elif key == curses.KEY_LEFT:
        return GameState.LEFT

    if key == curses.KEY_UP:
        return GameState.UP

    if key == curses.KEY_DOWN:
        return GameState.DOWN


def quit_game():
    curses.endwin()


class SnakeGame:
    COLOR_WHITE = 1
    COLOR_RED = 2

    GAME_SPEED = 0.075
    SNAKE_START_LEN = 1

    def __init__(self, dims):
        self.score = 0
        self.state = GameState(dims)
        # create screen
        self.scr = curses.initscr()

        # cursor and color config
        curses.curs_set(False)
        curses.noecho()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(self.COLOR_WHITE, curses.COLOR_WHITE,
                         curses.COLOR_WHITE)
        curses.init_pair(self.COLOR_RED, curses.COLOR_RED, curses.COLOR_RED)

        max_x, max_y = dims

        self.dim_x = max_x - 2
        self.dim_y = max_y - 2

        # add info
        self.scr.addstr(0, 1, 'SNAKE')
        quit_instructions = 'press ctrl-C to quit'
        score_meter = 'score %d ' % self.score
        if max_x - 2 < len(quit_instructions + score_meter):
            self.scr.addstr(self.dim_y + 1, 1, score_meter)
        else:
            self.scr.addstr(self.dim_y + 1, 1, score_meter +
                            ' ' * (self.dim_x - len(score_meter) - len(quit_instructions)) +
                            quit_instructions)

        # create window
        self.win = curses.newwin(self.dim_y, self.dim_x, 1, 1)
        self.win.keypad(True)
        self.win.box()
        self.win.timeout(int(self.GAME_SPEED * 1000))

        self.refresh()

    def run(self):
        # create snake
        self.render_snake()

        # create a food
        self.render_food(self.state.food_loc)

        # set current direction
        curr_key = curses.KEY_RIGHT
        while True:
            move = key_to_move(curr_key)
            self.erase_tail()
            self.score += self.state.make_move(move)
            self.erase_tail()

            if self.state.game_over:
                quit_game()
                return

            self.render_snake()
            self.render_food(self.state.food_loc)

            t = time.time()
            key = self.win.getch()
            if time.time() - t < self.GAME_SPEED:
                time.sleep(self.GAME_SPEED - (time.time() - t))
            if key != -1:
                if (is_allowed_key(key) and
                        not is_opposite_key(curr_key, key)):
                    curr_key = key

            self.refresh()

    def erase_tail(self):
        self.win.addch(self.state.snake.tail().y, self.state.snake.tail().x, ' ')

    def render_snake(self):
        self.win.addch(self.state.snake.head().y, self.state.snake.head().x, ' ',
                       curses.color_pair(self.COLOR_WHITE))
        self.win.addch(self.state.snake.tail().y, self.state.snake.tail().x, ' ',
                       curses.color_pair(self.COLOR_WHITE))

    def render_food(self, food):
        self.win.addch(food.y, food.x, ' ',
                       curses.color_pair(self.COLOR_RED))

    def refresh(self):
        # update score
        self.scr.addstr(self.dim_y + 1, 1, 'score: %d' % self.score)

        # refresh windows
        self.scr.refresh()
        self.win.refresh()


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
