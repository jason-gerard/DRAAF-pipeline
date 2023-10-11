import bchlib
import copy
import config


class BCHAdapter:

    def __init__(self):
        self.codec = bchlib.BCH(config.bch_config["num_ecc"], m=config.bch_config["m"])
        self.max_data_len = self.codec.n // 8 - (self.codec.ecc_bits + 7) // 8
        self.codec.data_len = config.data_packet_length_bits

    def encode(self, frame):
        frame_copy = bytearray(copy.deepcopy(frame))
        ecc = self.codec.encode(frame_copy)
        return frame + list(ecc)

    def decode(self, frame):
        frame_copy = copy.deepcopy(frame)
        data, ecc = bytearray(frame[:-self.codec.ecc_bytes]), bytearray(frame[-self.codec.ecc_bytes:])

        try:
            self.codec.decode(data, ecc)
            self.codec.correct(data, ecc)
            return list(data)
        except Exception as e:
            return frame_copy
