import glob
import os

import numpy as np
import tensorflow as tf
from tensorflow_core.python.keras.models import Model

import snake
from snake.agent.greedy_agent import GreedyAgent
from snake.model.model import create_model, board_preprocess
from snake.snake_game.game_state import GameState
from snake.snake_game.recorder import GameHistory, Recorder

CHECKPOINT_SAVE = 'checkpoint/model.chkpt'
DATA_DIR = 'data'
HISTORY_GLOB = f'data/*.npy'
REWARD_DECAY = 0.999

GAME_SHAPE = (32, 32)

AGENT_EPSILON = 0.85


def delete_random(prob):
    for game in glob.glob(HISTORY_GLOB):
        if np.random.rand() < prob:
            os.remove(game)


def main():
    fixed_model = create_model('fixed_model')
    model = create_model('training_model')

    while True:
        if os.path.exists(CHECKPOINT_SAVE):
            fixed_model.load_weights(CHECKPOINT_SAVE)
            model.load_weights(CHECKPOINT_SAVE)

        else:
            fixed_model.save_weights(CHECKPOINT_SAVE)
            model.load_weights(CHECKPOINT_SAVE)

        while True:
            avg_score = gen_games(fixed_model)
            print(f'AVG SCORE: {avg_score}')
            experience = tf.data.Dataset.from_generator(load_history,
                                                        output_types=(tf.float32, tf.float32, tf.float32, tf.float32),
                                                        output_shapes=(snake.model.model.input_dims, (4,), (),
                                                                       snake.model.model.input_dims))

            dataset = experience.shuffle(1000)
            dataset = dataset.batch(32)

            func = get_target_func(fixed_model)

            dataset = dataset.map(func)
            train_set = dataset.map(sep_train_features)
            target_set = dataset.map(sep_target)

            data = tf.data.Dataset.zip((train_set, target_set)).prefetch(1)

            model.fit(data, epochs=5)

            model.save(CHECKPOINT_SAVE)

            delete_random(0.05)


def sep_train_features(w, x, y, z):
    return w, x


def sep_target(w, x, y, z):
    return z


def get_target_func(model):
    def get_target(s_t, select_vector, r_t, s_t_1):
        batch_size = tf.shape(s_t_1)[0]
        selector = tf.ones((batch_size, 4), dtype=tf.float32)
        all_output, _ = model([s_t_1, selector])

        target = r_t + REWARD_DECAY * tf.reduce_max(all_output, axis=1)

        return s_t, select_vector, selector, target

    return get_target


def load_history():
    for fil in glob.glob(HISTORY_GLOB):
        game_history: GameHistory = np.load(fil, allow_pickle=True)[0]

        state = game_history.init_state

        prev_move = None

        for move in game_history.moves:

            s_t = board_preprocess(np.copy(state.frame_sequence.sequence))
            a_t = GameState.MOVES_DICT[move]
            a_t = tf.one_hot(a_t, len(GameState.MOVES), dtype=tf.float32)
            r_t = state.make_move(move)
            s_t_1 = board_preprocess(np.copy(state.frame_sequence.sequence))

            if move == prev_move and r_t == 1.0:
                # skip with prob 0.7
                if np.random.rand() < .7:
                    pass

            prev_move = move

            yield s_t, a_t, r_t, s_t_1


def gen_games(fixed_model: Model):
    games = sorted(glob.glob(HISTORY_GLOB))

    if len(games) < 50:
        num_missing = 50 - len(games)
    else:
        num_missing = 10
    print(f'Missing {num_missing} games')

    total_score = 0

    for i in range(num_missing):
        state = GameState(GAME_SHAPE)

        agent = GreedyAgent(state, fixed_model, AGENT_EPSILON)
        rec = Recorder(init_state=state)

        while not agent.state.game_over:
            move = agent.next_move()
            rec.add_move(move)
            agent.make_move(move)

        rec.write()
        total_score += agent.state.score

    return total_score / num_missing

    return 0


if __name__ == '__main__':
    main()
