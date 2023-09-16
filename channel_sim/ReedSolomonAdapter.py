from reedsolo import RSCodec
import copy

class ReedSolomonAdapter:

    def __init__(self):
        num_ecc = 10
        self.codec = RSCodec(num_ecc)

    def encode(self, frame):
        frame_copy = copy.deepcopy(frame)
        return self.codec.encode(frame_copy)

    def decode(self, frame):
        frame_copy = copy.deepcopy(frame)
        try:
            return list(self.codec.decode(frame_copy)[0])
        except:
            return frame_copy
