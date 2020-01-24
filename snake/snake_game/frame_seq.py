import numpy as np


class FrameSequence:
    def __init__(self, n, init_frame):
        self.n = n
        self.frame_shape = init_frame.shape
        self.sequence_shape = self.frame_shape[0], self.frame_shape[1], n
        self.sequence = np.zeros(self.sequence_shape, dtype=np.float32)

        for i in range(n):
            self.sequence[:, :, i] = init_frame

    def add_frame(self, frame):
        frame = np.copy(frame)
        for i in range(self.n - 1):
            self.sequence[:, :, i] = self.sequence[:, :, i + 1]

        self.sequence[:, :, self.n - 1] = frame

    def get_seq(self):
        return self.sequence
