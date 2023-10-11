import copy
from pyldpc import make_ldpc, decode, get_message, encode
import config
import numpy as np


class LDPCAdapter:

    def __init__(self):
        self.H, self.G = make_ldpc(config.ldpc_config["n"], config.ldpc_config["d_v"], config.ldpc_config["d_c"], systematic=True, sparse=True)
        n, self.k = self.G.shape

    def encode(self, frame, snr):
        frame_copy = copy.deepcopy(frame)
        output = []
        for offset in range(config.data_packet_length_bits // self.k):
            e = encode(self.G, frame_copy[offset*self.k:(offset+1)*self.k], snr)
            output += list(e)
        return output

    def decode(self, frame, snr):
        frame_copy = np.array(copy.deepcopy(frame))

        output = []
        for offset in range(config.data_packet_length_bits // self.k):
            d = decode(self.H, frame_copy[offset*self.k:(offset+1)*self.k], snr, maxiter=20)
            output += list(get_message(self.G, d))
        return output
