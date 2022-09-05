import cv2
import numpy as np

from nes import Rom
from movie import DoubleFrame

class MovieParser():
    lagFrames = [2527]

    def __init__(self, path):
        self.rom = Rom(path)
        self.state = DoubleFrame()
        self.prgBank = 0
        self.prgPtr = 0x8000
        self.chrBank = 0x10
        self.chrPtr = 0x1800
        self.mode = -1 # uninitialized
        self.modeData = -1 # uninitialized
        self.quadrant = -1 # uninitialized
        self.frame = 0 # distinct from quadrant because we can track lag frames

    def runFrame(self):
        self.frame += 1
        if self.frame in self.lagFrames:
            return self.frame
        if self.quadrant == 0:
            opcode = self.rom.get_prg_byte(self.prgBank, self.prgPtr)
            self.mode, self.modeData = self.getVideoOpcode(opcode)
            # advance pointer

    def getVideoOpcode(self, opcode):
        mode = (opcode & 0xC0) >> 6
        data = opcode & 0x3F
        return mode, data

    # mode 3
    def patchNametablePage(self):
        pass

    # mode 2
    def copyEntireNametable(self):
        pass

    # mode 1
    def freezeFrame(self):
        pass

    # mode 0
    def resetVideo(self):
        pass

    def processVideoInstruction(self, ptr):
        mode, data = getVideoOpcode(ptr)

def getNthFrame(n, path):
    parser = MovieParser(path)
    if n < 8:
        return np.full((480, 512, 3), (0,255,0), np.uint8)
    return np.full((480, 512, 3), (0,255,0), np.uint8)

if __name__ == '__main__':
    bad_apple = MovieParser('./bad_apple_2_5.nes')
