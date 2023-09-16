import random
import copy


class Channel:
    def __init__(self, BER):
        self.BER = BER
        self.inverse_BER = 1 / BER

    def frame_factory(self, num_bits):
        return [random.randint(0, 1) for _ in range(num_bits)]

    def broadcast_frame(self, frame):
        frame_copy = copy.deepcopy(frame)
        for i in range(len(frame_copy)):
            sample = random.randrange(0, int(self.inverse_BER))
            if sample == 0:
                frame_copy[i] = int(not frame_copy[i])

        return frame_copy
