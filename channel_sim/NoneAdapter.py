import copy

class NoneAdapter:
    def encode(self, frame, _):
        frame_copy = copy.deepcopy(frame)
        return frame_copy

    def decode(self, frame, _):
        frame_copy = copy.deepcopy(frame)
        return frame_copy
