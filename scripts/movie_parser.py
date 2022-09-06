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
    lag_frames = [2527]

    def __init__(self, path):
        self.rom = Rom(path)
        self.state = DoubleFrame()
        self.reset_video()
        self.frame_count = 4 # distinct from quadrant because we can track lag frames
        self.commands = [self.reset_video, self.freeze_frame, self.copy_entire_nametable, self.patchNametablePage]

    def run_frame(self):
        if self.frame_count == 4:
            self.get_video_opcode()
            assert CommandMode(self.mode) == CommandMode.REPLACE, 'expected 2, got ' + str(self.mode)
            for _ in range(4):
                self.copy_entire_nametable()
                self.quadrant = (self.quadrant + 1) % 4
            self.frame_count = 8
            return self.frame_count, self.quadrant
        if self.frame_count in self.lag_frames:
            self.frame_count += 1
            return self.frame_count, self.quadrant
        if CommandMode(self.mode) == CommandMode.FREEZE:
            if self.quadrant > 0:
                self.frame_count += 1
                self.quadrant = (self.quadrant + 1) % 4
                return self.frame_count, self.quadrant
            else:
                self.mode_data -= 1
                if self.mode_data > 0:
                    self.frame_count += 1
                    self.quadrant = (self.quadrant + 1) % 4
                    return self.frame_count, self.quadrant
        if self.quadrant == 0:
            self.get_video_opcode()
        # run command if needed
        self.commands[self.mode]()
        self.quadrant = (self.quadrant + 1) % 4
        self.frame_count += 1
        return self.frame_count, self.quadrant

    def get_video_opcode(self):
        opcode = self.rom.get_prg_byte(*self.prg_ptr.advance())
        self.mode = (opcode & 0xC0) >> 6
        self.mode_data = opcode & 0x3F

    # mode 3
    def patchNametablePage(self):
        assert self.mode_data < 16, 'Probably parsing error'
        # check if quadrant(?) has updates
        update_quad = self.mode_data % 2
        self.mode_data //= 2
        if update_quad == 0:
            return
        # fillBuffer loop
        slice_changes = []
        for _ in range(4):
            byte = self.rom.get_prg_byte(*self.prg_ptr.advance())
            slice_changes.append(byte)
        # whileBufferHasOnBits
        for i in range(8):
            for j in range(4):
                should_patch_slice = (slice_changes[j] & 0x80) >> 7
                slice_changes[j] = (slice_changes[j] << 1) & 0xFF
                if should_patch_slice == 1:
                    self._patch_slice(self.quadrant, i, j)

    def _patch_slice(self, quad, y, x):
        new_y = 8*quad + y
        new_x = 8*x
        tiles_to_patch = self.rom.get_chr_byte(*self.chr_ptr.advance())
        # print(f'CHR Data: {tiles_to_patch:02X}')
        for i in range(8):
            should_patch_tile = (tiles_to_patch >> (7-i)) & 1
            if should_patch_tile == 1:
                newTile = self.rom.get_prg_byte(*self.prg_ptr.advance())
                self.state.patch((new_y, new_x), newTile)
            new_x += 1

    # mode 2
    def copy_entire_nametable(self):
        copy = 0x100
        if self.quadrant == 3:
            copy = 0xC0
        for i in range(copy):
            byte = self.rom.get_prg_byte(*self.prg_ptr.advance())
            index = self.quadrant * 0x100 + i
            y = index // 32
            x = index % 32
            self.state.patch((y,x), byte)

    # mode 1
    def freeze_frame(self):
        return

    # mode 0
    def reset_video(self):
        self.prg_ptr = RomPointer(0, 0x8000, 0xA000)
        self.chr_ptr = RomPointer(0x10, 0x1800, 0x1C00)
        self.mode = 0 # uninitialized
        self.mode_data = 0 # uninitialized
        self.quadrant = 0 # uninitialized


def get_nth_frame(n, parser):
    if n < 9:
        return np.full((480, 512, 3), (11,72,0), np.uint8)
    frame = parser.state.copy()
    quadrant = 0
    frame_num = parser.frame_count
    # kind of horrible, should fix
    while frame_num < n - 2:
        frame_num, quadrant = parser.run_frame()
        if quadrant == 0:
            frame = parser.state.copy()
    frame0, frame1 = frame.export()
    if quadrant < 2:
        return frame0
    return frame1

if __name__ == '__main__':
    bad_apple = MovieParser('./bad_apple_2_5.nes')
    length = 13141
    test_frame = 92
    codec = cv2.VideoWriter.fourcc(*'mp4v')
    movie = cv2.VideoWriter('bad_apple_v1.mp4', codec, 60, (512,480))
    for i in range(length):
        frame = get_nth_frame(i, bad_apple)
        movie.write(frame)
        if i % 100 == 0:
            print(i, 'frames')

