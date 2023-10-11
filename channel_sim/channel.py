import copy
from enum import Enum
import numpy as np


class State(Enum):
    good = 1
    bad = 2


# This channel is based on a Gilbert-Elliot model for modeling burst errors, there is a
# good and bad state which have different bit error rates
class Channel:
    def __init__(self, gBER, bBER):
        self.gBER = gBER
        self.bBER = bBER
        self.state = State.good

    def frame_factory(self, num_bits):
        frame = [0 for _ in range(num_bits)]
        frame[0] = 1
        return frame

    def broadcast_frame(self, frame):
        frame_copy = copy.deepcopy(frame)
        for i in range(len(frame_copy)):
            # 0 -> no error, 1 -> error
            BER = self.gBER if self.state == State.good else self.bBER
            sample = np.random.choice([0, 1], 1, p=[1 - BER, BER])[0]
            is_error = sample == 1
            if is_error:
                frame_copy[i] = 1
                self.state = State.bad
            else:
                self.state = State.good

        self.state = State.good
        return frame_copy
