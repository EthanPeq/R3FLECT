import time

class VisionState:
    def __init__(self):
        self.recognized_name = None
        self.last_detected_time = None
        self.swipe_mode_active = False
        self.prev_index_x = None
        self.prev_time = time.time()