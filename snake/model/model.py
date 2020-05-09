import numpy as np
import tensorflow as tf
from tensorflow import keras

from snake.snake_game import game_state

input_dims = (32, 32, 3)

NUM_CLASSES = 4
DECODER_UNITS = 32


def residual_depthwise_block(x, num_repeats):
    residual = x
    for i in range(num_repeats):
        x = keras.layers.DepthwiseConv2D(3, padding='same', strides=1, activation='relu',
                                         kernel_regularizer=tf.keras.regularizers.l2(0.01))(x)

    return keras.layers.Add()([x, residual])


def create_model(name='q_learning_model'):
    model_input = keras.Input(shape=input_dims, name='input_frames')
    selection_input = keras.Input(shape=(NUM_CLASSES,))

    x = model_input

    x = residual_depthwise_block(x, 2)
    x = residual_depthwise_block(x, 2)

    x = keras.layers.Conv2D(16, 1, strides=1, padding='valid', activation='relu')(x)
    x = keras.layers.Conv2D(32, 3, strides=2, padding='valid', activation='relu')(x)
    x = keras.layers.Conv2D(64, 3, strides=2, padding='valid', activation='relu')(x)

    encoding = x

    encoder_out = keras.layers.GlobalAveragePooling2D()(encoding)

    y = encoder_out
    y = keras.layers.Dense(DECODER_UNITS, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))(y)
    y = keras.layers.Dense(NUM_CLASSES, activation=None, name='output',
                           kernel_regularizer=tf.keras.regularizers.l2(0.01))(y)

    output = y
    selected_output = tf.math.reduce_sum(selection_input * y, axis=1)

    model = keras.Model(inputs=[model_input, selection_input], outputs=[output, selected_output], name=name)

    model.compile(optimizer='adam', loss=[None, 'mse'], metrics=['mae'])

    # print("Creating new model:")
    # model.summary()
    return model


def compute_target(target_model):
    pass


def board_preprocess(board):
    board = np.copy(board)

    mask = board == game_state.FOOD_SYMBOL
    board[mask] = 1000

    mask = board == game_state.BODY_SYMBOL
    board[mask] = -100

    mask = board == game_state.HEAD_SYMBOL
    board[mask] = -1000

    return board
