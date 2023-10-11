from reedsolo import RSCodec
import copy
import config


class ReedSolomonAdapter:

    def __init__(self):
        self.codec = RSCodec(config.rs_config["num_ecc"])

    def encode(self, frame, _):
        frame_copy = copy.deepcopy(frame)
        return self.codec.encode(frame_copy)

    def decode(self, frame, _):
        frame_copy = copy.deepcopy(frame)
        try:
            return list(self.codec.decode(frame_copy)[0])
        except:
            return frame_copy
