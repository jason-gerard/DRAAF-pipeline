import copy
from ldpc.codes import rep_code
from ldpc import bp_decoder


class LDPCAdapter:

    def __init__(self):
        n = 504
        self.H = rep_code(n)
        self.codec = bp_decoder(self.H, bp_method="product_sum")

    def encode(self, frame):
        frame_copy = copy.deepcopy(frame)
        return frame_copy

    def decode(self, frame):
        frame_copy = copy.deepcopy(frame)
        syndrome = self.H @ frame_copy % 2
        return list(self.codec.decode(syndrome))
