import random
import copy


class Channel:
    def __init__(self, BER):
        self.BER = BER
        self.inverse_BER = 1 / BER

    def frame_factory(self, num_bits):
        return [0 for _ in range(num_bits)]

    def broadcast_frame(self, frame):
        frame_copy = copy.deepcopy(frame)
        for i in range(len(frame_copy)):
            sample = random.randrange(0, int(self.inverse_BER))
            is_error = sample == 0
            if is_error:
                frame_copy[i] = 1

        return frame_copy
