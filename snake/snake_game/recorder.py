import copy
import os
import time

import numpy as np

from snake.snake_game.game_state import GameState


class Recorder:
    def __init__(self, init_state: GameState, save_dir='data'):
        self.save_dir = save_dir
        self.history = GameHistory(copy.deepcopy(init_state))
        self.moves = []

    def add_move(self, move):
        self.history.moves.append(move)

    def write(self):
        timestamp = str(int(time.time() * 1000))
        save_file = os.path.join(self.save_dir, timestamp)
        np.save(save_file, np.array([self.history]))


class GameHistory:
    def __init__(self, init_state: GameState):
        self.init_state = init_state
        self.moves = []

    def __str__(self):
        return str(self.moves)
