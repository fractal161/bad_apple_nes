from PIL import Image
import numpy as np

'''
Technically consists of two frames by design.
'''
class MovieFrame():
    def __init__(self, *args, **kwargs):
        pass
    def patch_frame(self):
        pass
    def export(self):
        pass

class Movie():
    def __init__(self, *args, **kwargs):
        pass
    def export(self):
        pass

if __name__ == '__main__':
    test_frame = MovieFrame()
    frame1, frame2 = test_frame.export()
    frame1.show()
    frame2.show()
