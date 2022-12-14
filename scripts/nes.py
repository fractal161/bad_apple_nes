
# taken from https://github.com/qalle2/nes-util/blob/main/qneslib.py
PALETTE = {
    0x00: (0x74, 0x74, 0x74),
    0x01: (0x24, 0x18, 0x8c),
    0x02: (0x00, 0x00, 0xa8),
    0x03: (0x44, 0x00, 0x9c),
    0x04: (0x8c, 0x00, 0x74),
    0x05: (0xa8, 0x00, 0x10),
    0x06: (0xa4, 0x00, 0x00),
    0x07: (0x7c, 0x08, 0x00),
    0x08: (0x40, 0x2c, 0x00),
    0x09: (0x00, 0x44, 0x00),
    0x0a: (0x00, 0x50, 0x00),
    0x0b: (0x00, 0x3c, 0x14),
    0x0c: (0x18, 0x3c, 0x5c),
    0x0d: (0x00, 0x00, 0x00),
    0x0e: (0x00, 0x00, 0x00),
    0x0f: (0x00, 0x00, 0x00),
    0x10: (0xbc, 0xbc, 0xbc),
    0x11: (0x00, 0x70, 0xec),
    0x12: (0x20, 0x38, 0xec),
    0x13: (0x80, 0x00, 0xf0),
    0x14: (0xbc, 0x00, 0xbc),
    0x15: (0xe4, 0x00, 0x58),
    0x16: (0xd8, 0x28, 0x00),
    0x17: (0xc8, 0x4c, 0x0c),
    0x18: (0x88, 0x70, 0x00),
    0x19: (0x00, 0x94, 0x00),
    0x1a: (0x00, 0xa8, 0x00),
    0x1b: (0x00, 0x90, 0x38),
    0x1c: (0x00, 0x80, 0x88),
    0x1d: (0x00, 0x00, 0x00),
    0x1e: (0x00, 0x00, 0x00),
    0x1f: (0x00, 0x00, 0x00),
    0x20: (0xfc, 0xfc, 0xfc),
    0x21: (0x3c, 0xbc, 0xfc),
    0x22: (0x5c, 0x94, 0xfc),
    0x23: (0xcc, 0x88, 0xfc),
    0x24: (0xf4, 0x78, 0xfc),
    0x25: (0xfc, 0x74, 0xb4),
    0x26: (0xfc, 0x74, 0x60),
    0x27: (0xfc, 0x98, 0x38),
    0x28: (0xf0, 0xbc, 0x3c),
    0x29: (0x80, 0xd0, 0x10),
    0x2a: (0x4c, 0xdc, 0x48),
    0x2b: (0x58, 0xf8, 0x98),
    0x2c: (0x00, 0xe8, 0xd8),
    0x2d: (0x78, 0x78, 0x78),
    0x2e: (0x00, 0x00, 0x00),
    0x2f: (0x00, 0x00, 0x00),
    0x30: (0xfc, 0xfc, 0xfc),
    0x31: (0xa8, 0xe4, 0xfc),
    0x32: (0xc4, 0xd4, 0xfc),
    0x33: (0xd4, 0xc8, 0xfc),
    0x34: (0xfc, 0xc4, 0xfc),
    0x35: (0xfc, 0xc4, 0xd8),
    0x36: (0xfc, 0xbc, 0xb0),
    0x37: (0xfc, 0xd8, 0xa8),
    0x38: (0xfc, 0xe4, 0xa0),
    0x39: (0xe0, 0xfc, 0xa0),
    0x3a: (0xa8, 0xf0, 0xbc),
    0x3b: (0xb0, 0xfc, 0xcc),
    0x3c: (0x9c, 0xfc, 0xf0),
    0x3d: (0xc4, 0xc4, 0xc4),
    0x3e: (0x00, 0x00, 0x00),
    0x3f: (0x00, 0x00, 0x00),
}

class Rom():
    def __init__(self, path):
        with open(path, 'rb') as f:
            rom = f.read()
        self.header = self._get_header_from_bytes(rom[0:16])
        start = 16
        self.trainer = b''
        if self.header['trainer']:
            self.trainer = rom[16:528]
            start += 0x200
        self.prg = rom[start:start+self.header['prg_size']]
        start += self.header['prg_size']
        self.chr = rom[start:start+self.header['chr_size']]
        start += self.header['chr_size']

    # assumes ines1.0, doesn't look at flags 7-15 really
    def _get_header_from_bytes(self, header_bytes):
        byte_list = list(header_bytes)
        header = {}
        header['prg_size'] = 0x4000 * byte_list[4]
        header['chr_size'] = 0x2000 * byte_list[5]
        header['mapper'] = byte_list[7] & 0xF0 + (byte_list[6] >> 4)
        header['mirroring'] = byte_list[6] & 1
        header['battery'] = bool((byte_list[6] >> 1) & 1)
        header['trainer'] = bool((byte_list[6] >> 2) & 1)
        header['four_screen'] = bool((byte_list[6] >> 3) & 1)
        return header

    # assuming each bank is 8kb because mmc3
    def get_prg_byte(self, bank, addr):
        return self.prg[bank * 0x2000 + (addr % 0x2000)]

    # assuming each bank is 1kb (works for our case)
    def get_chr_byte(self, bank, addr):
        return self.chr[bank * 0x400 + (addr % 0x400)]

class RomPointer():
    def __init__(self, start_bank, start_addr, max_addr):
        self.bank = start_bank
        self.start_bank = start_bank
        self.addr = start_addr
        self.start_addr = start_addr
        self.max_addr = max_addr
    def get(self):
        return self.bank, self.addr
    def advance(self):
        bank = self.bank
        addr = self.addr
        self.addr += 1
        if self.addr == self.max_addr:
            self.addr = self.start_addr
            self.bank += 1
        return bank, addr

    def reset(self):
        self.bank = self.start_bank
        self.addr = self.start_addr

if __name__ == '__main__':
    test_rom = Rom('./bad_apple_2_5.nes')


