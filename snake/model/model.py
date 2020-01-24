import tensorflow as tf
from tensorflow import keras

input_dims = (32, 32, 3)

NUM_CLASSES = 4
DECODER_UNITS = 32


def create_model(name='q_learning_model'):
    model_input = keras.Input(shape=input_dims, name='input_frames')
    selection_input = keras.Input(shape=(NUM_CLASSES,))

    x = model_input

    x = keras.layers.Conv2D(32, 3, padding='same', strides=1, activation='relu')(x)
    x = keras.layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)
    x = keras.layers.Conv2D(64, 3, padding='same', strides=1, activation='relu')(x)
    x = keras.layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)

    encoding = x

    encoder_out = keras.layers.GlobalAveragePooling2D()(encoding)

    y = encoder_out
    y = keras.layers.Dense(DECODER_UNITS, activation='relu')(y)
    y = keras.layers.Dense(NUM_CLASSES, activation=None, name='output')(y)

    output = y
    selected_output = tf.math.reduce_sum(selection_input * y, axis=1)

    model = keras.Model(inputs=[model_input, selection_input], outputs=[output, selected_output], name=name)

    model.compile(optimizer='adam', loss=[None, 'mse'], metrics=['mae'])

    # print("Creating new model:")
    # model.summary()
    return model


def compute_target(target_model):
    pass
