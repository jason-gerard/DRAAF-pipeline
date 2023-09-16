import copy

class NoneAdapter:
    def encode(self, frame):
        frame_copy = copy.deepcopy(frame)
        return frame_copy

    def decode(self, frame):
        frame_copy = copy.deepcopy(frame)
        return frame_copy
