import glob
import os

import numpy as np
import tensorflow as tf

import snake
from snake.model.model import create_model
from snake.snake_game.game_state import GameState
from snake.snake_game.recorder import GameHistory

CHECKPOINT_SAVE = 'checkpoint/model.chkpt'
DATA_DIR = 'data'
HISTORY_GLOB = f'data/*.npy'
REWARD_DECAY = 0.2


def main():
    fixed_model = create_model('fixed_model')
    model = create_model('training_model')

    if os.path.exists(CHECKPOINT_SAVE):
        fixed_model.load_weights(CHECKPOINT_SAVE)
        model.load_weights(CHECKPOINT_SAVE)

    else:
        fixed_model.save_weights(CHECKPOINT_SAVE)
        model.load_weights(CHECKPOINT_SAVE)

    experience = tf.data.Dataset.from_generator(load_history,
                                                output_types=(tf.float32, tf.float32, tf.float32, tf.float32),
                                                output_shapes=(snake.model.model.input_dims, (4,), (),
                                                               snake.model.model.input_dims))

    dataset = experience.shuffle(1000, reshuffle_each_iteration=True)
    dataset = dataset.batch(32)

    func = get_target_func(fixed_model)

    dataset = dataset.map(func)
    train_set = dataset.map(abcd)
    target_set = dataset.map(efgh)

    data = tf.data.Dataset.zip((train_set, target_set)).prefetch(1)
    print(data)
    model.summary()
    model.fit(data, epochs=100)

    model.save(CHECKPOINT_SAVE)


def final(w, x, y, z):
    print(w)
    print(x)
    print(y)
    print(z)
    return w, x,


def abcd(w, x, y, z):
    return w, x


def efgh(w, x, y, z):
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

        for move in game_history.moves:
            s_t = np.copy(state.frame_sequence.sequence)
            a_t = GameState.MOVES_DICT[move]
            a_t = tf.one_hot(a_t, len(GameState.MOVES), dtype=tf.float32)
            r_t = state.make_move(move)
            s_t_1 = np.copy(state.frame_sequence.sequence)

            yield s_t, a_t, r_t, s_t_1


if __name__ == '__main__':
    main()
