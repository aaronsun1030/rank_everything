class Scaling:
    def __init__(self):
        self.WINDOW_HEIGHT = 900
        self.WINDOW_WIDTH = 1600
        self.FRAME_SIZE_800 = 800
        self.FRAME_SIZE_700 = 700
        self.FRAME_SIZE_600 = 600
        self.FRAME_SIZE_300 = 300
        self.SCALE_SIZE_60 = 60
        self.SCALE_SIZE_30 = 30
        self.SCALE_SIZE_10 = 10


    def scaleTo(self, multiplier):
        self.WINDOW_HEIGHT = int(self.WINDOW_HEIGHT * multiplier) 
        self.WINDOW_WIDTH = int(self.WINDOW_WIDTH * multiplier)
        self.FRAME_SIZE_800 = int(self.FRAME_SIZE_800 * multiplier)
        self.FRAME_SIZE_700 = int(self.FRAME_SIZE_700 * multiplier)
        self.FRAME_SIZE_600 = int(self.FRAME_SIZE_600 * multiplier)
        self.FRAME_SIZE_300 = int(self.FRAME_SIZE_300 * multiplier)
        self.SCALE_SIZE_60 = int(self.SCALE_SIZE_60 * multiplier)
        self.SCALE_SIZE_30 = int(self.SCALE_SIZE_30 * multiplier)
        self.SCALE_SIZE_10 = int(self.SCALE_SIZE_10 * multiplier / 2)

