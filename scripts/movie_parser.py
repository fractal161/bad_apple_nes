import cv2
import numpy as np
from enum import Enum

from nes import Rom, RomPointer
from movie import DoubleFrame

class CommandMode(Enum):
    RESET = 0
    FREEZE = 1
    REPLACE = 2
    PATCH = 3

class MovieParser():
    lagFrames = [2527]

    def __init__(self, path):
        self.rom = Rom(path)
        self.state = DoubleFrame()
        self.resetVideo()
        self.frameCount = 4 # distinct from quadrant because we can track lag frames
        self.commands = [self.resetVideo, self.freezeFrame, self.copyEntireNametable, self.patchNametablePage]

    def runFrame(self):
        if self.frameCount == 4:
            self.getVideoOpcode()
            assert CommandMode(self.mode) == CommandMode.REPLACE, 'expected 2, got ' + str(self.mode)
            for _ in range(4):
                self.copyEntireNametable()
                self.quadrant = (self.quadrant + 1) % 4
            self.frameCount = 8
            return self.frameCount
        if self.frameCount in self.lagFrames:
            self.frameCount += 1
            return self.frameCount
        if CommandMode(self.mode) == CommandMode.FREEZE:
            if self.quadrant > 0:
                self.frameCount += 1
                self.quadrant = (self.quadrant + 1) % 4
                return self.frameCount
            else:
                self.modeData -= 1
                if self.modeData > 0:
                    self.frameCount += 1
                    self.quadrant = (self.quadrant + 1) % 4
                    return self.frameCount
        if self.quadrant == 0:
            self.getVideoOpcode()
        # run command if needed
        self.commands[self.mode]()
        self.quadrant = (self.quadrant + 1) % 4
        self.frameCount += 1
        return self.frameCount

    def getVideoOpcode(self):
        opcode = self.rom.get_prg_byte(*self.prgPtr.advance())
        self.mode = (opcode & 0xC0) >> 6
        self.modeData = opcode & 0x3F

    # mode 3
    def patchNametablePage(self):
        assert self.modeData < 16, 'Probably parsing error'
        # check if quadrant(?) has updates
        updateQuad = self.modeData % 2
        self.modeData //= 2
        if updateQuad == 0:
            return
        # fillBuffer loop
        sliceChanges = []
        for _ in range(4):
            byte = self.rom.get_prg_byte(*self.prgPtr.advance())
            sliceChanges.append(byte)
        # whileBufferHasOnBits
        for i in range(8):
            for j in range(4):
                shouldPatchSlice = (sliceChanges[j] & 0x80) >> 7
                sliceChanges[j] = (sliceChanges[j] << 1) & 0xFF
                if shouldPatchSlice == 1:
                    self._patchSlice(self.quadrant, i, j)

    def _patchSlice(self, quad, y, x):
        newY = 8*quad + y
        newX = 8*x
        tilesToPatch = self.rom.get_chr_byte(*self.chrPtr.advance())
        # print(f'CHR Data: {tilesToPatch:02X}')
        for i in range(8):
            shouldPatchTile = (tilesToPatch >> (7-i)) & 1
            if shouldPatchTile == 1:
                newTile = self.rom.get_prg_byte(*self.prgPtr.advance())
                self.state.patch((newY, newX), newTile)
            newX += 1

    # mode 2
    def copyEntireNametable(self):
        copy = 0x100
        if self.quadrant == 3:
            copy = 0xC0
        for i in range(copy):
            byte = self.rom.get_prg_byte(*self.prgPtr.advance())
            index = self.quadrant * 0x100 + i
            y = index // 32
            x = index % 32
            self.state.patch((y,x), byte)

    # mode 1
    def freezeFrame(self):
        return

    # mode 0
    def resetVideo(self):
        self.prgPtr = RomPointer(0, 0x8000, 0xA000)
        self.chrPtr = RomPointer(0x10, 0x1800, 0x1C00)
        self.mode = 0 # uninitialized
        self.modeData = 0 # uninitialized
        self.quadrant = 0 # uninitialized


def getNthFrame(n, path):
    parser = MovieParser(path)
    if n < 8:
        return np.full((480, 512, 3), (0,255,0), np.uint8)
    return np.full((480, 512, 3), (0,255,0), np.uint8)

if __name__ == '__main__':
    bad_apple = MovieParser('./bad_apple_2_5.nes')
    length = 13141
    frame = 0
    while frame <= 13141:
        frame = bad_apple.runFrame()

