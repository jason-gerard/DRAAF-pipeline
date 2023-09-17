import copy
import numpy as np

BERs = [
    1 * 10 ** -0,  # 1 i.e. every bit is an error
    1 * 10 ** -1,  # 0.1 10% of bits are errors
    1 * 10 ** -2,  # 0.01
    1 * 10 ** -3,
    1 * 10 ** -4,
    2 * 10 ** -4,
    1 * 10 ** -5,
    1 * 10 ** -6,
    0,  # No errors
]


class Channel:
    def __init__(self, BER):
        self.BER = BER

    def frame_factory(self, num_bits):
        return [0 for _ in range(num_bits)]

    def broadcast_frame(self, frame):
        frame_copy = copy.deepcopy(frame)
        for i in range(len(frame_copy)):
            # 0 -> no error, 1 -> error
            sample = np.random.choice([0, 1], 1, p=[1 - self.BER, self.BER])[0]
            is_error = sample == 1
            if is_error:
                frame_copy[i] = 1

        return frame_copy
