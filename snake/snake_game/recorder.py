import copy
import os
import time

import numpy as np


class Recorder:
    def __init__(self, init_state, save_dir='data'):
        self.save_dir = save_dir
        self.history = GameHistory(copy.deepcopy(init_state))
        self.moves = []

    def add_move(self, move):
        self.history.moves.append(move)

    def write(self):
        timestamp = str(int(time.time()))
        save_file = os.path.join(self.save_dir, timestamp)
        np.save(save_file, self.history)


class GameHistory:
    def __init__(self, init_state):
        self.init_state = init_state
        self.moves = []
