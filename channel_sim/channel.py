import copy
import numpy as np


class Channel:
    def __init__(self, ber):
        self.ber = ber

    def frame_factory(self, num_bits):
        return [0 for _ in range(num_bits)]

    def broadcast_frame(self, frame):
        # 0 -> no error, 1 -> error
        samples = np.random.choice([0, 1], size=len(frame), p=[1 - self.ber, self.ber])
        for sample in samples:
            if sample == 1:
                return True

        return False
