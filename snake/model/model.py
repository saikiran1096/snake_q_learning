from tensorflow import keras

input_dims = (32, 32, 3)

NUM_CLASSES = 4


def create_model():
    model_input = keras.Input(shape=input_dims, name='input_frames')
    x = model_input

    x = keras.layers.Conv2D(32, 3, padding='same', strides=1, activation='relu')(x)
    x = keras.layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)
    x = keras.layers.Conv2D(64, 3, padding='same', strides=1, activation='relu')(x)
    x = keras.layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)

    encoding = x

    y = keras.layers.GlobalAveragePooling2D()(encoding)
    decoder_out = keras.layers.Dense(NUM_CLASSES, activation=None)(y)

    model = keras.Model(inputs=model_input, outputs=decoder_out, name='q_learning_model')

    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    print("Creating new model:")
    model.summary()
    return model
