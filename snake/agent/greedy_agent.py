import random
import numpy as np

import snake.model.model
from snake.snake_game.game_state import GameState


class GreedyAgent:
    def __init__(self, init_state: GameState, model, eps):
        self.state = init_state
        self.eps = eps
        self.model = model

    def next_move(self):
        x = np.random.random_sample()

        if x < self.eps:
            return random.choice(GameState.MOVES)

        else:
            seq = self.state.frame_sequence.sequence
            seq = snake.model.model.board_preprocess(seq)
            seq = seq.reshape((1, 32, 32, 3))
            _select = np.zeros((1, 4))

            q, _ = self.model([seq, _select])
            ind = np.argmax(q)
            move = GameState.MOVES[ind]

            return move

    def make_move(self, move):
        self.state.make_move(move)
